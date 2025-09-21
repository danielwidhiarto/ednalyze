import sys
import json
import numpy as np
import pandas as pd
from tensorflow.keras.models import load_model
from sklearn.preprocessing import MinMaxScaler
import warnings
warnings.filterwarnings('ignore')

def get_tf_config(timeframe):
    config_map = {
        '5m': {       # 🔪 SCALPING
            'limit': 1500,            # ~5 hari data
            'sequence_len': 60,       # 5 jam input
            'forward': 6              # prediksi 30 menit ke depan
        },
        '15m': {      # ⚡ INTRADAY
            'limit': 2000,            # ~20 hari data
            'sequence_len': 64,       # 16 jam input
            'forward': 4              # prediksi 1 jam ke depan
        },
        '1h': {       # ⚖️ HYBRID / Default
            'limit': 2000,
            'sequence_len': 48,       # 2 hari input
            'forward': 3              # prediksi 3 jam ke depan
        },
        '4h': {       # 🎯 SWING
            'limit': 1000,            # ~6 bulan data
            'sequence_len': 32,       # ~5 hari input
            'forward': 2              # prediksi 8 jam ke depan
        },
        '1d': {       # 📦 POSITION
            'limit': 700,             # ~2 tahun data
            'sequence_len': 30,       # 1 bulan input
            'forward': 2              # prediksi 2 hari ke depan
        }
    }
    return config_map.get(timeframe, config_map['1h'])  # default ke 1h kalau gak ketemu

def add_technical_features(df):
    """Add technical indicators to dataframe"""
    df = df.copy()
    
    # Moving averages
    df['ema14'] = df['close'].ewm(span=14).mean()
    df['ema50'] = df['close'].ewm(span=50).mean()
    
    # RSI calculation
    delta = df['close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    df['rsi'] = 100 - (100 / (1 + rs))
    
    # Volatility (ATR approximation)
    df['volatility'] = (df['high'] - df['low']).rolling(window=14).mean()
    
    # Price momentum
    df['momentum'] = df['close'].pct_change(7)
    
    # Volume indicators
    df['volume_sma'] = df['volume'].rolling(window=20).mean()
    df['volume_ratio'] = df['volume'] / df['volume_sma']
    
    # Candlestick patterns (simplified)
    df['body_size'] = abs(df['close'] - df['open'])
    df['upper_shadow'] = df['high'] - df[['close', 'open']].max(axis=1)
    df['lower_shadow'] = df[['close', 'open']].min(axis=1) - df['low']
    
    # Engulfing pattern (simplified)
    df['engulfing'] = 0
    for i in range(1, len(df)):
        if (df.iloc[i]['close'] > df.iloc[i]['open'] and  # Current bullish
            df.iloc[i-1]['close'] < df.iloc[i-1]['open'] and  # Previous bearish
            df.iloc[i]['open'] < df.iloc[i-1]['close'] and  # Current open below prev close
            df.iloc[i]['close'] > df.iloc[i-1]['open']):  # Current close above prev open
            df.iloc[i, df.columns.get_loc('engulfing')] = 1
    
    # Doji pattern (simplified)
    df['doji'] = (df['body_size'] / (df['high'] - df['low']) < 0.1).astype(int)
    
    # Simplified BOS and FVG indicators
    df['BOS'] = 0
    df['FVG'] = 0
    
    # BOS: Simple breakout detection
    df['high_20'] = df['high'].rolling(window=20).max()
    df['low_20'] = df['low'].rolling(window=20).min()
    df['BOS'] = ((df['close'] > df['high_20'].shift(1)) | 
                 (df['close'] < df['low_20'].shift(1))).astype(int)
    
    # FVG: Gap detection (simplified)
    df['gap'] = abs(df['open'] - df['close'].shift(1))
    df['avg_gap'] = df['gap'].rolling(window=20).mean()
    df['FVG'] = (df['gap'] > df['avg_gap'] * 2).astype(int)
    
    return df

def explain_reason(df, index=-1):
    """Generate explanation for prediction"""
    row = df.iloc[index]
    reasons = []
    active_signals = 0

    if row.get('engulfing', 0) == 1:
        reasons.append("Terdeteksi pola Bullish Engulfing")
        active_signals += 1
    if row.get('doji', 0) == 1:
        reasons.append("Candle Doji menunjukkan kebimbangan market")
        active_signals += 1
    if row.get('ema14', 0) > row.get('ema50', 0):
        reasons.append("EMA 14 berada di atas EMA 50 (tren naik jangka pendek)")
        active_signals += 1
    if row.get('rsi', 0) > 60:
        reasons.append(f"RSI tinggi ({row['rsi']:.1f}) menunjukkan tekanan beli")
        active_signals += 1
    elif row.get('rsi', 0) < 40:
        reasons.append(f"RSI rendah ({row['rsi']:.1f}) menunjukkan tekanan jual")
        active_signals += 1
    if row.get('BOS', 0) == 1:
        reasons.append("Break of Structure terkonfirmasi")
        active_signals += 1
    if row.get('FVG', 0) == 1:
        reasons.append("Fair Value Gap aktif di sekitar harga")
        active_signals += 1

    # LEVEL 1: Skor Teknis
    score_pct = active_signals / 6 * 100
    if active_signals >= 4:
        rating = f"Sinyal teknikal **KUAT** ({active_signals}/6 indikator aktif = {score_pct:.0f}%)"
    elif active_signals >= 2:
        rating = f"Sinyal teknikal **MODERAT** ({active_signals}/6 indikator aktif = {score_pct:.0f}%)"
    elif active_signals == 1:
        rating = f"Sinyal teknikal **LEMAH** (1/6 indikator aktif = 17%)"
    else:
        rating = "Tidak ada sinyal teknikal dominan"

    # LEVEL 2: Summary Kalimat Natural
    if active_signals == 0:
        summary = "Model memprediksi arah market tanpa dukungan sinyal teknikal dominan."
    else:
        summary = f"Model memprediksi arah market dengan dukungan {active_signals} indikator aktif seperti: " + "; ".join(reasons[:3]) + ("." if len(reasons) <= 3 else ", dll.")

    return reasons, rating, summary, score_pct

def preprocess_coingecko_data(data):
    """Convert CoinGecko data to dataframe format"""
    try:
        # Convert historical prices to OHLCV format (simplified)
        prices = data['historical_prices']
        volumes = data['historical_volumes']
        
        df_data = []
        for i in range(len(prices)):
            timestamp = pd.to_datetime(prices[i][0], unit='ms')
            price = float(prices[i][1])
            volume = float(volumes[i][1]) if i < len(volumes) else 0
            
            # Create OHLC from single price (approximation)
            # In real scenario, you'd need proper OHLCV data
            volatility_factor = 0.02  # 2% volatility approximation
            high = price * (1 + volatility_factor)
            low = price * (1 - volatility_factor)
            open_price = price
            close = price
            
            df_data.append({
                'timestamp': timestamp,
                'open': open_price,
                'high': high,
                'low': low,
                'close': close,
                'volume': volume
            })
        
        df = pd.DataFrame(df_data)
        df = df.sort_values('timestamp').reset_index(drop=True)
        
        return df
    except Exception as e:
        raise ValueError(f"Error preprocessing CoinGecko data: {str(e)}")

def predict_direction_advanced(model, df_raw, timeframe='1h'):
    """Advanced prediction with technical analysis"""
    try:
        cfg = get_tf_config(timeframe)
        
        # Add technical features
        df_feat = add_technical_features(df_raw.copy()).dropna()
        
        if len(df_feat) < cfg['sequence_len']:
            raise ValueError(f"Not enough data for {timeframe} timeframe. Need {cfg['sequence_len']}, got {len(df_feat)}")
        
        # Feature columns for model
        feature_cols = [
            'close', 'volume', 'ema14', 'ema50', 'rsi', 'volatility', 
            'momentum', 'volume_ratio', 'body_size', 'upper_shadow', 
            'lower_shadow'
        ]
        
        # Ensure all feature columns exist
        for col in feature_cols:
            if col not in df_feat.columns:
                df_feat[col] = 0
        
        # Scale features
        scaler = MinMaxScaler()
        df_scaled = df_feat.copy()
        df_scaled[feature_cols] = scaler.fit_transform(df_feat[feature_cols])
        
        # Prepare sequence input
        seq_input = df_scaled[feature_cols].iloc[-cfg['sequence_len']:].values
        seq_input = np.expand_dims(seq_input, axis=0)
        
        # Make prediction
        pred_prob = model.predict(seq_input, verbose=0)
        
        # Handle different model output formats
        if pred_prob.shape[1] == 3:  # 3-class model (SHORT, WAIT, LONG)
            pred_class = np.argmax(pred_prob, axis=1)[0]
            label_map = {0: 'SHORT', 1: 'WAIT', 2: 'LONG'}
            probs = {
                'SHORT': float(pred_prob[0][0]),
                'WAIT': float(pred_prob[0][1]),
                'LONG': float(pred_prob[0][2])
            }
        else:  # Binary model (assuming 0=down, 1=up)
            probability = float(pred_prob[0][0])
            if probability > 0.6:
                pred_class = 2  # LONG
            elif probability < 0.4:
                pred_class = 0  # SHORT
            else:
                pred_class = 1  # WAIT
            
            label_map = {0: 'SHORT', 1: 'WAIT', 2: 'LONG'}
            probs = {
                'SHORT': 1 - probability,
                'WAIT': abs(0.5 - probability) * 2,
                'LONG': probability
            }
        
        direction = label_map[pred_class]
        
        return direction, probs, df_feat
        
    except Exception as e:
        raise ValueError(f"Error in advanced prediction: {str(e)}")

def generate_trading_plan(direction, probs, df_feat, timeframe='1h'):
    """Generate trading plan with entry, SL, TP"""
    try:
        # Get last candle data
        last_candle = df_feat.iloc[-1]
        price = last_candle['close']
        atr = last_candle.get('volatility', abs(last_candle['high'] - last_candle['low']))
        
        # Risk management based on timeframe
        risk_multipliers = {
            '5m': {'sl': 0.3, 'tp': 0.6},
            '15m': {'sl': 0.5, 'tp': 1.0},
            '1h': {'sl': 0.8, 'tp': 1.5},
            '4h': {'sl': 1.2, 'tp': 2.0},
            '1d': {'sl': 2.0, 'tp': 3.0}
        }
        
        multiplier = risk_multipliers.get(timeframe, risk_multipliers['1h'])
        sl_buffer = atr * multiplier['sl']
        tp_buffer = atr * multiplier['tp']
        
        if direction == 'LONG':
            entry = price
            sl = price - sl_buffer
            tp = price + tp_buffer
        elif direction == 'SHORT':
            entry = price
            sl = price + sl_buffer
            tp = price - tp_buffer
        else:  # WAIT
            entry = price
            sl = tp = None
        
        # Generate reasons and analysis
        reasons, rating, summary, score_pct = explain_reason(df_feat)
        
        # Determine confidence level
        max_prob = max(probs.values())
        if max_prob > 0.8:
            confidence_level = "VERY HIGH"
        elif max_prob > 0.65:
            confidence_level = "HIGH"
        elif max_prob > 0.55:
            confidence_level = "MEDIUM"
        else:
            confidence_level = "LOW"
        
        result = {
            'timeframe': timeframe,
            'direction': direction,
            'confidence_level': confidence_level,
            'probabilities': {
                'SHORT': round(probs['SHORT'] * 100, 2),
                'WAIT': round(probs['WAIT'] * 100, 2),
                'LONG': round(probs['LONG'] * 100, 2)
            },
            'trading_plan': {
                'entry': round(entry, 6),
                'stop_loss': round(sl, 6) if sl else None,
                'take_profit': round(tp, 6) if tp else None
            },
            'technical_analysis': {
                'reasons': reasons,
                'rating': rating,
                'summary': summary,
                'signal_strength': round(score_pct, 1)
            }
        }
        
        return result
        
    except Exception as e:
        raise ValueError(f"Error generating trading plan: {str(e)}")

def main():
    try:
        # Read input data
        input_data = json.loads(sys.argv[1])
        
        # Load model
        model = load_model('/Users/danielwidhiarto/Projects/EDnalyze/backend/ai-service/ednalyze_model.keras')
        
        # Convert CoinGecko data to proper format
        df_raw = preprocess_coingecko_data(input_data)
        
        # Determine timeframe (default to 1h)
        timeframe = input_data.get('timeframe', '1h')
        
        # Make advanced prediction
        direction, probs, df_feat = predict_direction_advanced(model, df_raw, timeframe)
        
        # Generate comprehensive trading plan
        analysis = generate_trading_plan(direction, probs, df_feat, timeframe)
        
        # Add coin-specific information
        analysis['coin_info'] = {
            'id': input_data.get('coin_id', 'unknown'),
            'current_price': input_data.get('current_price', 0),
            'market_cap': input_data.get('market_cap', 0),
            'volume_24h': input_data.get('volume_24h', 0)
        }
        
        # Output result
        print(json.dumps(analysis))
        
    except Exception as e:
        error_result = {
            "error": str(e),
            "direction": "UNKNOWN",
            "confidence_level": "LOW",
            "probabilities": {
                "SHORT": 0,
                "WAIT": 100,
                "LONG": 0
            },
            "trading_plan": {
                "entry": 0,
                "stop_loss": None,
                "take_profit": None
            },
            "technical_analysis": {
                "reasons": ["Error in analysis"],
                "rating": "ERROR",
                "summary": f"Analysis failed: {str(e)}",
                "signal_strength": 0
            }
        }
        print(json.dumps(error_result))
        sys.exit(1)

if __name__ == "__main__":
    main()