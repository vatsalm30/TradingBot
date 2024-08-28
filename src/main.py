from secret import secrets
import ccxt

exchange = ccxt.binance(
{
    'options': {
        'adjustForTimeDifference': True,
        'defaultType': 'future',
    },
    'apiKey': secrets["apiKey"],
    'secret': secrets["secret"],
    'enableRateLimit': True,
})

exchange.set_sandbox_mode(True)
