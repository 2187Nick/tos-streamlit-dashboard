# Option Volume x OHLC Cumulative
# Twitter @2187Nick
# Feb 10, 2025

declare lower;
declare once_per_bar;
input strikeSpacing = 1.0;
input strikes = 20; # max 20
input ManuallySetExpiration = {default "false", "true"};
input Expiration_YYMMDD = 250221;

def CurrentYear = GetYear() - 2000;
def CurrentMonth = GetMonth();
def CurrentDOM = GetDayOfMonth(GetYYYYMMDD());
def DateString_auto = CurrentYear * 10000 + CurrentMonth * 100 + CurrentDOM;

def DateString = if manuallysetexpiration then Expiration_YYMMDD else  DateString_auto;

DefineGlobalColor("CallColor", Color.GREEN);
DefineGlobalColor("PutColor", Color.RED);
AddLabel(yes, AsPrice(DateString) + "C", GlobalColor("CallColor"));
AddLabel(yes, AsPrice(DateString) + "P", GlobalColor("PutColor"));

def agg = AggregationPeriod.DAY;
def openlevel = open(period = agg);
def rounding_factor = if strikeSpacing > 1 and strikeSpacing < 25 then -1 else if strikeSpacing > 24 then -2 else 0;
def floor_or_ceiling =  Round(openlevel, rounding_factor);
def base_strike = floor_or_ceiling;

def strike_base = base_strike;
def strike_plus1 = base_strike + strikeSpacing;
def strike_plus2 = base_strike + strikeSpacing * 2;
def strike_plus3 = base_strike + strikeSpacing * 3;
def strike_plus4 = base_strike + strikeSpacing * 4;
def strike_plus5 = base_strike + strikeSpacing * 5;
def strike_plus6 = base_strike + strikeSpacing * 6;
def strike_plus7 = base_strike + strikeSpacing * 7;
def strike_plus8 = base_strike + strikeSpacing * 8;
def strike_plus9 = base_strike + strikeSpacing * 9;
def strike_plus10 = base_strike + strikeSpacing * 10;
def strike_plus11 = base_strike + strikeSpacing * 11;
def strike_plus12 = base_strike + strikeSpacing * 12;
def strike_plus13 = base_strike + strikeSpacing * 13;
def strike_plus14 = base_strike + strikeSpacing * 14;
def strike_plus15 = base_strike + strikeSpacing * 15;
def strike_plus16 = base_strike + strikeSpacing * 16;
def strike_plus17 = base_strike + strikeSpacing * 17;
def strike_plus18 = base_strike + strikeSpacing * 18;
def strike_plus19 = base_strike + strikeSpacing * 19;
def strike_plus20 = base_strike + strikeSpacing * 20;
def strike_plus21 = base_strike + strikeSpacing * 21;

def strike_minus1 = base_strike - strikeSpacing;
def strike_minus2 = base_strike - strikeSpacing * 2;
def strike_minus3 = base_strike - strikeSpacing * 3;
def strike_minus4 = base_strike - strikeSpacing * 4;
def strike_minus5 = base_strike - strikeSpacing * 5;
def strike_minus6 = base_strike - strikeSpacing * 6;
def strike_minus7 = base_strike - strikeSpacing * 7;
def strike_minus8 = base_strike - strikeSpacing * 8;
def strike_minus9 = base_strike - strikeSpacing * 9;
def strike_minus10 = base_strike - strikeSpacing * 10;
def strike_minus11 = base_strike - strikeSpacing * 11;
def strike_minus12 = base_strike - strikeSpacing * 12;
def strike_minus13 = base_strike - strikeSpacing * 13;
def strike_minus14 = base_strike - strikeSpacing * 14;
def strike_minus15 = base_strike - strikeSpacing * 15;
def strike_minus16 = base_strike - strikeSpacing * 16;
def strike_minus17 = base_strike - strikeSpacing * 17;
def strike_minus18 = base_strike - strikeSpacing * 18;
def strike_minus19 = base_strike - strikeSpacing * 19;
def strike_minus20 = base_strike - strikeSpacing * 20;
def strike_minus21 = base_strike - strikeSpacing * 21;

### Put Option Volume
def putOptionVolume = if IsNaN(volume("." + GetSymbol() + AsPrice(DateString) + "P" + AsPrice(strike_base))) then 0 else volume("." + GetSymbol() + AsPrice(DateString) + "P" + AsPrice(strike_base));
def putOptionVolume1 =  if strikes < 1 then 0 else if IsNaN(volume("." + GetSymbol() + AsPrice(DateString) + "P" + AsPrice(strike_minus1))) then 0 else volume("." + GetSymbol() + AsPrice(DateString) + "P" + AsPrice(strike_minus1));
def putOptionVolume2 =  if strikes < 2 then 0 else if IsNaN(volume("." + GetSymbol() + AsPrice(DateString) + "P" + AsPrice(strike_minus2))) then 0 else volume("." + GetSymbol() + AsPrice(DateString) + "P" + AsPrice(strike_minus2));
def putOptionVolume3 =  if strikes < 3 then 0 else if IsNaN(volume("." + GetSymbol() + AsPrice(DateString) + "P" + AsPrice(strike_minus3))) then 0 else volume("." + GetSymbol() + AsPrice(DateString) + "P" + AsPrice(strike_minus3));
def putOptionVolume4 = if strikes < 4 then 0 else if isNaN(volume("." + GetSymbol() + AsPrice(DateString) + "P" + AsPrice(strike_minus4))) then 0 else volume("." + GetSymbol() + AsPrice(DateString) + "P" + AsPrice(strike_minus4));
def putOptionVolume5 = if strikes < 5 then 0 else if isNaN(volume("." + GetSymbol() + AsPrice(DateString) + "P" + AsPrice(strike_minus5))) then 0 else volume("." + GetSymbol() + AsPrice(DateString) + "P" + AsPrice(strike_minus5));
def putOptionVolume6 = if strikes < 6 then 0 else if isNaN(volume("." + GetSymbol() + AsPrice(DateString) + "P" + AsPrice(strike_minus6))) then 0 else volume("." + GetSymbol() + AsPrice(DateString) + "P" + AsPrice(strike_minus6));
def putOptionVolume7 = if strikes < 7 then 0 else if isNaN(volume("." + GetSymbol() + AsPrice(DateString) + "P" + AsPrice(strike_minus7))) then 0 else volume("." + GetSymbol() + AsPrice(DateString) + "P" + AsPrice(strike_minus7));
def putOptionVolume8 = if strikes < 8 then 0 else if isNaN(volume("." + GetSymbol() + AsPrice(DateString) + "P" + AsPrice(strike_minus8))) then 0 else volume("." + GetSymbol() + AsPrice(DateString) + "P" + AsPrice(strike_minus8));
def putOptionVolume9 = if strikes < 9 then 0 else if isNaN(volume("." + GetSymbol() + AsPrice(DateString) + "P" + AsPrice(strike_minus9))) then 0 else volume("." + GetSymbol() + AsPrice(DateString) + "P" + AsPrice(strike_minus9));
def putOptionVolume10 = if strikes < 10 then 0 else if isNaN(volume("." + GetSymbol() + AsPrice(DateString) + "P" + AsPrice(strike_minus10))) then 0 else volume("." + GetSymbol() + AsPrice(DateString) + "P" + AsPrice(strike_minus10));
def putOptionVolume11 = if strikes < 11 then 0 else if isNaN(volume("." + GetSymbol() + AsPrice(DateString) + "P" + AsPrice(strike_minus11))) then 0 else volume("." + GetSymbol() + AsPrice(DateString) + "P" + AsPrice(strike_minus11));
def putOptionVolume12 = if strikes < 12 then 0 else if isNaN(volume("." + GetSymbol() + AsPrice(DateString) + "P" + AsPrice(strike_minus12))) then 0 else volume("." + GetSymbol() + AsPrice(DateString) + "P" + AsPrice(strike_minus12));
def putOptionVolume13 = if strikes < 13 then 0 else if isNaN(volume("." + GetSymbol() + AsPrice(DateString) + "P" + AsPrice(strike_minus13))) then 0 else volume("." + GetSymbol() + AsPrice(DateString) + "P" + AsPrice(strike_minus13));
def putOptionVolume14 = if strikes < 14 then 0 else if isNaN(volume("." + GetSymbol() + AsPrice(DateString) + "P" + AsPrice(strike_minus14))) then 0 else volume("." + GetSymbol() + AsPrice(DateString) + "P" + AsPrice(strike_minus14));
def putOptionVolume15 = if strikes < 15 then 0 else if isNaN(volume("." + GetSymbol() + AsPrice(DateString) + "P" + AsPrice(strike_minus15))) then 0 else volume("." + GetSymbol() + AsPrice(DateString) + "P" + AsPrice(strike_minus15));
def putOptionVolume16 = if strikes < 16 then 0 else if isNaN(volume("." + GetSymbol() + AsPrice(DateString) + "P" + AsPrice(strike_minus16))) then 0 else volume("." + GetSymbol() + AsPrice(DateString) + "P" + AsPrice(strike_minus16));
def putOptionVolume17 = if strikes < 17 then 0 else if isNaN(volume("." + GetSymbol() + AsPrice(DateString) + "P" + AsPrice(strike_minus17))) then 0 else volume("." + GetSymbol() + AsPrice(DateString) + "P" + AsPrice(strike_minus17));
def putOptionVolume18 = if strikes < 18 then 0 else if isNaN(volume("." + GetSymbol() + AsPrice(DateString) + "P" + AsPrice(strike_minus18))) then 0 else volume("." + GetSymbol() + AsPrice(DateString) + "P" + AsPrice(strike_minus18));
def putOptionVolume19 = if strikes < 19 then 0 else if isNaN(volume("." + GetSymbol() + AsPrice(DateString) + "P" + AsPrice(strike_minus19))) then 0 else volume("." + GetSymbol() + AsPrice(DateString) + "P" + AsPrice(strike_minus19));
def putOptionVolume20 = if strikes < 20 then 0 else if isNaN(volume("." + GetSymbol() + AsPrice(DateString) + "P" + AsPrice(strike_minus20))) then 0 else volume("." + GetSymbol() + AsPrice(DateString) + "P" + AsPrice(strike_minus20));


def putOptionVolume1a =  if strikes < 1 then 0 else if IsNaN(volume("." + GetSymbol() + AsPrice(DateString) + "P" + AsPrice(strike_plus1))) then 0 else volume("." + GetSymbol() + AsPrice(DateString) + "P" + AsPrice(strike_plus1));
def putOptionVolume2a =  if strikes < 2 then 0 else if IsNaN(volume("." + GetSymbol() + AsPrice(DateString) + "P" + AsPrice(strike_plus2))) then 0 else volume("." + GetSymbol() + AsPrice(DateString) + "P" + AsPrice(strike_plus2));
def putOptionVolume3a =  if strikes < 3 then 0 else if IsNaN(volume("." + GetSymbol() + AsPrice(DateString) + "P" + AsPrice(strike_plus3))) then 0 else volume("." + GetSymbol() + AsPrice(DateString) + "P" + AsPrice(strike_plus3));
def putOptionVolume4a = if strikes < 4 then 0 else if isNaN(volume("." + GetSymbol() + AsPrice(DateString) + "P" + AsPrice(strike_plus4))) then 0 else volume("." + GetSymbol() + AsPrice(DateString) + "P" + AsPrice(strike_plus4));
def putOptionVolume5a = if strikes < 5 then 0 else if isNaN(volume("." + GetSymbol() + AsPrice(DateString) + "P" + AsPrice(strike_plus5))) then 0 else volume("." + GetSymbol() + AsPrice(DateString) + "P" + AsPrice(strike_plus5));
def putOptionVolume6a = if strikes < 6 then 0 else if isNaN(volume("." + GetSymbol() + AsPrice(DateString) + "P" + AsPrice(strike_plus6))) then 0 else volume("." + GetSymbol() + AsPrice(DateString) + "P" + AsPrice(strike_plus6));
def putOptionVolume7a = if strikes < 7 then 0 else if isNaN(volume("." + GetSymbol() + AsPrice(DateString) + "P" + AsPrice(strike_plus7))) then 0 else volume("." + GetSymbol() + AsPrice(DateString) + "P" + AsPrice(strike_plus7));
def putOptionVolume8a = if strikes < 8 then 0 else if isNaN(volume("." + GetSymbol() + AsPrice(DateString) + "P" + AsPrice(strike_plus8))) then 0 else volume("." + GetSymbol() + AsPrice(DateString) + "P" + AsPrice(strike_plus8));
def putOptionVolume9a = if strikes < 9 then 0 else if isNaN(volume("." + GetSymbol() + AsPrice(DateString) + "P" + AsPrice(strike_plus9))) then 0 else volume("." + GetSymbol() + AsPrice(DateString) + "P" + AsPrice(strike_plus9));
def putOptionVolume10a = if strikes < 10 then 0 else if isNaN(volume("." + GetSymbol() + AsPrice(DateString) + "P" + AsPrice(strike_plus10))) then 0 else volume("." + GetSymbol() + AsPrice(DateString) + "P" + AsPrice(strike_plus10));
def putOptionVolume11a = if strikes < 11 then 0 else if isNaN(volume("." + GetSymbol() + AsPrice(DateString) + "P" + AsPrice(strike_plus11))) then 0 else volume("." + GetSymbol() + AsPrice(DateString) + "P" + AsPrice(strike_plus11));
def putOptionVolume12a = if strikes < 12 then 0 else if isNaN(volume("." + GetSymbol() + AsPrice(DateString) + "P" + AsPrice(strike_plus12))) then 0 else volume("." + GetSymbol() + AsPrice(DateString) + "P" + AsPrice(strike_plus12));
def putOptionVolume13a = if strikes < 13 then 0 else if isNaN(volume("." + GetSymbol() + AsPrice(DateString) + "P" + AsPrice(strike_plus13))) then 0 else volume("." + GetSymbol() + AsPrice(DateString) + "P" + AsPrice(strike_plus13));
def putOptionVolume14a = if strikes < 14 then 0 else if isNaN(volume("." + GetSymbol() + AsPrice(DateString) + "P" + AsPrice(strike_plus14))) then 0 else volume("." + GetSymbol() + AsPrice(DateString) + "P" + AsPrice(strike_plus14));
def putOptionVolume15a = if strikes < 15 then 0 else if isNaN(volume("." + GetSymbol() + AsPrice(DateString) + "P" + AsPrice(strike_plus15))) then 0 else volume("." + GetSymbol() + AsPrice(DateString) + "P" + AsPrice(strike_plus15));
def putOptionVolume16a = if strikes < 16 then 0 else if isNaN(volume("." + GetSymbol() + AsPrice(DateString) + "P" + AsPrice(strike_plus16))) then 0 else volume("." + GetSymbol() + AsPrice(DateString) + "P" + AsPrice(strike_plus16));
def putOptionVolume17a = if strikes < 17 then 0 else if isNaN(volume("." + GetSymbol() + AsPrice(DateString) + "P" + AsPrice(strike_plus17))) then 0 else volume("." + GetSymbol() + AsPrice(DateString) + "P" + AsPrice(strike_plus17));
def putOptionVolume18a = if strikes < 18 then 0 else if isNaN(volume("." + GetSymbol() + AsPrice(DateString) + "P" + AsPrice(strike_plus18))) then 0 else volume("." + GetSymbol() + AsPrice(DateString) + "P" + AsPrice(strike_plus18));
def putOptionVolume19a = if strikes < 19 then 0 else if isNaN(volume("." + GetSymbol() + AsPrice(DateString) + "P" + AsPrice(strike_plus19))) then 0 else volume("." + GetSymbol() + AsPrice(DateString) + "P" + AsPrice(strike_plus19));
def putOptionVolume20a = if strikes < 20 then 0 else if isNaN(volume("." + GetSymbol() + AsPrice(DateString) + "P" + AsPrice(strike_plus20))) then 0 else volume("." + GetSymbol() + AsPrice(DateString) + "P" + AsPrice(strike_plus20));

###Call Option Volume
def callOptionVolume = if IsNaN(volume("." + GetSymbol() + AsPrice(DateString) + "C" + AsPrice(strike_base))) then 0 else volume("." + GetSymbol() + AsPrice(DateString) + "C" + AsPrice(strike_base));
def callOptionVolume1 =  if strikes < 1 then 0 else if IsNaN(volume("." + GetSymbol() + AsPrice(DateString) + "C" + AsPrice(strike_plus1))) then 0 else volume("." + GetSymbol() + AsPrice(DateString) + "C" + AsPrice(strike_plus1));
def callOptionVolume2 =  if strikes < 2 then 0 else if IsNaN(volume("." + GetSymbol() + AsPrice(DateString) + "C" + AsPrice(strike_plus2))) then 0 else volume("." + GetSymbol() + AsPrice(DateString) + "C" + AsPrice(strike_plus2));
def callOptionVolume3 =  if strikes < 3 then 0 else if IsNaN(volume("." + GetSymbol() + AsPrice(DateString) + "C" + AsPrice(strike_plus3))) then 0 else volume("." + GetSymbol() + AsPrice(DateString) + "C" + AsPrice(strike_plus3));
def callOptionVolume4 = if strikes < 4 then 0 else if isNaN(volume("." + GetSymbol() + AsPrice(DateString) + "C" + AsPrice(strike_plus4))) then 0 else volume("." + GetSymbol() + AsPrice(DateString) + "C" + AsPrice(strike_plus4));
def callOptionVolume5 = if strikes < 5 then 0 else if isNaN(volume("." + GetSymbol() + AsPrice(DateString) + "C" + AsPrice(strike_plus5))) then 0 else volume("." + GetSymbol() + AsPrice(DateString) + "C" + AsPrice(strike_plus5));
def callOptionVolume6 = if strikes < 6 then 0 else if isNaN(volume("." + GetSymbol() + AsPrice(DateString) + "C" + AsPrice(strike_plus6))) then 0 else volume("." + GetSymbol() + AsPrice(DateString) + "C" + AsPrice(strike_plus6));
def callOptionVolume7 = if strikes < 7 then 0 else if isNaN(volume("." + GetSymbol() + AsPrice(DateString) + "C" + AsPrice(strike_plus7))) then 0 else volume("." + GetSymbol() + AsPrice(DateString) + "C" + AsPrice(strike_plus7));
def callOptionVolume8 = if strikes < 8 then 0 else if isNaN(volume("." + GetSymbol() + AsPrice(DateString) + "C" + AsPrice(strike_plus8))) then 0 else volume("." + GetSymbol() + AsPrice(DateString) + "C" + AsPrice(strike_plus8));
def callOptionVolume9 = if strikes < 9 then 0 else if isNaN(volume("." + GetSymbol() + AsPrice(DateString) + "C" + AsPrice(strike_plus9))) then 0 else volume("." + GetSymbol() + AsPrice(DateString) + "C" + AsPrice(strike_plus9));
def callOptionVolume10 = if strikes < 10 then 0 else if isNaN(volume("." + GetSymbol() + AsPrice(DateString) + "C" + AsPrice(strike_plus10))) then 0 else volume("." + GetSymbol() + AsPrice(DateString) + "C" + AsPrice(strike_plus10));
def callOptionVolume11 = if strikes < 11 then 0 else if isNaN(volume("." + GetSymbol() + AsPrice(DateString) + "C" + AsPrice(strike_plus11))) then 0 else volume("." + GetSymbol() + AsPrice(DateString) + "C" + AsPrice(strike_plus11));
def callOptionVolume12 = if strikes < 12 then 0 else if isNaN(volume("." + GetSymbol() + AsPrice(DateString) + "C" + AsPrice(strike_plus12))) then 0 else volume("." + GetSymbol() + AsPrice(DateString) + "C" + AsPrice(strike_plus12));
def callOptionVolume13 = if strikes < 13 then 0 else if isNaN(volume("." + GetSymbol() + AsPrice(DateString) + "C" + AsPrice(strike_plus13))) then 0 else volume("." + GetSymbol() + AsPrice(DateString) + "C" + AsPrice(strike_plus13));
def callOptionVolume14 = if strikes < 14 then 0 else if isNaN(volume("." + GetSymbol() + AsPrice(DateString) + "C" + AsPrice(strike_plus14))) then 0 else volume("." + GetSymbol() + AsPrice(DateString) + "C" + AsPrice(strike_plus14));
def callOptionVolume15 = if strikes < 15 then 0 else if isNaN(volume("." + GetSymbol() + AsPrice(DateString) + "C" + AsPrice(strike_plus15))) then 0 else volume("." + GetSymbol() + AsPrice(DateString) + "C" + AsPrice(strike_plus15));
def callOptionVolume16 = if strikes < 16 then 0 else if isNaN(volume("." + GetSymbol() + AsPrice(DateString) + "C" + AsPrice(strike_plus16))) then 0 else volume("." + GetSymbol() + AsPrice(DateString) + "C" + AsPrice(strike_plus16));
def callOptionVolume17 = if strikes < 17 then 0 else if isNaN(volume("." + GetSymbol() + AsPrice(DateString) + "C" + AsPrice(strike_plus17))) then 0 else volume("." + GetSymbol() + AsPrice(DateString) + "C" + AsPrice(strike_plus17));
def callOptionVolume18 = if strikes < 18 then 0 else if isNaN(volume("." + GetSymbol() + AsPrice(DateString) + "C" + AsPrice(strike_plus18))) then 0 else volume("." + GetSymbol() + AsPrice(DateString) + "C" + AsPrice(strike_plus18));
def callOptionVolume19 = if strikes < 19 then 0 else if isNaN(volume("." + GetSymbol() + AsPrice(DateString) + "C" + AsPrice(strike_plus19))) then 0 else volume("." + GetSymbol() + AsPrice(DateString) + "C" + AsPrice(strike_plus19));
def callOptionVolume20 = if strikes < 20 then 0 else if isNaN(volume("." + GetSymbol() + AsPrice(DateString) + "C" + AsPrice(strike_plus20))) then 0 else volume("." + GetSymbol() + AsPrice(DateString) + "C" + AsPrice(strike_plus20));

def callOptionVolume1a =  if strikes < 1 then 0 else if IsNaN(volume("." + GetSymbol() + AsPrice(DateString) + "C" + AsPrice(strike_minus1))) then 0 else volume("." + GetSymbol() + AsPrice(DateString) + "C" + AsPrice(strike_minus1));
def callOptionVolume2a =  if strikes < 2 then 0 else if IsNaN(volume("." + GetSymbol() + AsPrice(DateString) + "C" + AsPrice(strike_minus2))) then 0 else volume("." + GetSymbol() + AsPrice(DateString) + "C" + AsPrice(strike_minus2));
def callOptionVolume3a =  if strikes < 3 then 0 else if IsNaN(volume("." + GetSymbol() + AsPrice(DateString) + "C" + AsPrice(strike_minus3))) then 0 else volume("." + GetSymbol() + AsPrice(DateString) + "C" + AsPrice(strike_minus3));
def callOptionVolume4a = if strikes < 4 then 0 else if isNaN(volume("." + GetSymbol() + AsPrice(DateString) + "C" + AsPrice(strike_minus4))) then 0 else volume("." + GetSymbol() + AsPrice(DateString) + "C" + AsPrice(strike_minus4));
def callOptionVolume5a = if strikes < 5 then 0 else if isNaN(volume("." + GetSymbol() + AsPrice(DateString) + "C" + AsPrice(strike_minus5))) then 0 else volume("." + GetSymbol() + AsPrice(DateString) + "C" + AsPrice(strike_minus5));
def callOptionVolume6a = if strikes < 6 then 0 else if isNaN(volume("." + GetSymbol() + AsPrice(DateString) + "C" + AsPrice(strike_minus6))) then 0 else volume("." + GetSymbol() + AsPrice(DateString) + "C" + AsPrice(strike_minus6));
def callOptionVolume7a = if strikes < 7 then 0 else if isNaN(volume("." + GetSymbol() + AsPrice(DateString) + "C" + AsPrice(strike_minus7))) then 0 else volume("." + GetSymbol() + AsPrice(DateString) + "C" + AsPrice(strike_minus7));
def callOptionVolume8a = if strikes < 8 then 0 else if isNaN(volume("." + GetSymbol() + AsPrice(DateString) + "C" + AsPrice(strike_minus8))) then 0 else volume("." + GetSymbol() + AsPrice(DateString) + "C" + AsPrice(strike_minus8));
def callOptionVolume9a = if strikes < 9 then 0 else if isNaN(volume("." + GetSymbol() + AsPrice(DateString) + "C" + AsPrice(strike_minus9))) then 0 else volume("." + GetSymbol() + AsPrice(DateString) + "C" + AsPrice(strike_minus9));
def callOptionVolume10a = if strikes < 10 then 0 else if isNaN(volume("." + GetSymbol() + AsPrice(DateString) + "C" + AsPrice(strike_minus10))) then 0 else volume("." + GetSymbol() + AsPrice(DateString) + "C" + AsPrice(strike_minus10));
def callOptionVolume11a = if strikes < 11 then 0 else if isNaN(volume("." + GetSymbol() + AsPrice(DateString) + "C" + AsPrice(strike_minus11))) then 0 else volume("." + GetSymbol() + AsPrice(DateString) + "C" + AsPrice(strike_minus11));
def callOptionVolume12a = if strikes < 12 then 0 else if isNaN(volume("." + GetSymbol() + AsPrice(DateString) + "C" + AsPrice(strike_minus12))) then 0 else volume("." + GetSymbol() + AsPrice(DateString) + "C" + AsPrice(strike_minus12));
def callOptionVolume13a = if strikes < 13 then 0 else if isNaN(volume("." + GetSymbol() + AsPrice(DateString) + "C" + AsPrice(strike_minus13))) then 0 else volume("." + GetSymbol() + AsPrice(DateString) + "C" + AsPrice(strike_minus13));
def callOptionVolume14a = if strikes < 14 then 0 else if isNaN(volume("." + GetSymbol() + AsPrice(DateString) + "C" + AsPrice(strike_minus14))) then 0 else volume("." + GetSymbol() + AsPrice(DateString) + "C" + AsPrice(strike_minus14));
def callOptionVolume15a = if strikes < 15 then 0 else if isNaN(volume("." + GetSymbol() + AsPrice(DateString) + "C" + AsPrice(strike_minus15))) then 0 else volume("." + GetSymbol() + AsPrice(DateString) + "C" + AsPrice(strike_minus15));
def callOptionVolume16a = if strikes < 16 then 0 else if isNaN(volume("." + GetSymbol() + AsPrice(DateString) + "C" + AsPrice(strike_minus16))) then 0 else volume("." + GetSymbol() + AsPrice(DateString) + "C" + AsPrice(strike_minus16));
def callOptionVolume17a = if strikes < 17 then 0 else if isNaN(volume("." + GetSymbol() + AsPrice(DateString) + "C" + AsPrice(strike_minus17))) then 0 else volume("." + GetSymbol() + AsPrice(DateString) + "C" + AsPrice(strike_minus17));
def callOptionVolume18a = if strikes < 18 then 0 else if isNaN(volume("." + GetSymbol() + AsPrice(DateString) + "C" + AsPrice(strike_minus18))) then 0 else volume("." + GetSymbol() + AsPrice(DateString) + "C" + AsPrice(strike_minus18));
def callOptionVolume19a = if strikes < 19 then 0 else if isNaN(volume("." + GetSymbol() + AsPrice(DateString) + "C" + AsPrice(strike_minus19))) then 0 else volume("." + GetSymbol() + AsPrice(DateString) + "C" + AsPrice(strike_minus19));
def callOptionVolume20a = if strikes < 20 then 0 else if isNaN(volume("." + GetSymbol() + AsPrice(DateString) + "C" + AsPrice(strike_minus20))) then 0 else volume("." + GetSymbol() + AsPrice(DateString) + "C" + AsPrice(strike_minus20));

### Put Option ohlc4
def putOptionohlc4 = if IsNaN(ohlc4("." + GetSymbol() + AsPrice(DateString) + "P" + AsPrice(strike_base))) then 0 else ohlc4("." + GetSymbol() + AsPrice(DateString) + "P" + AsPrice(strike_base));
def putOptionohlc41 =  if strikes < 1 then 0 else if IsNaN(ohlc4("." + GetSymbol() + AsPrice(DateString) + "P" + AsPrice(strike_minus1))) then 0 else ohlc4("." + GetSymbol() + AsPrice(DateString) + "P" + AsPrice(strike_minus1));
def putOptionohlc42 =  if strikes < 2 then 0 else if IsNaN(ohlc4("." + GetSymbol() + AsPrice(DateString) + "P" + AsPrice(strike_minus2))) then 0 else ohlc4("." + GetSymbol() + AsPrice(DateString) + "P" + AsPrice(strike_minus2));
def putOptionohlc43 = if strikes < 3 then 0 else if IsNaN(ohlc4("." + GetSymbol() + AsPrice(DateString) + "P" + AsPrice(strike_minus3))) then 0 else ohlc4("." + GetSymbol() + AsPrice(DateString) + "P" + AsPrice(strike_minus3));
def putOptionohlc44 = if strikes < 4 then 0 else if IsNaN(ohlc4("." + GetSymbol() + AsPrice(DateString) + "P" + AsPrice(strike_minus4))) then 0 else ohlc4("." + GetSymbol() + AsPrice(DateString) + "P" + AsPrice(strike_minus4));
def putOptionohlc45 = if strikes < 5 then 0 else if IsNaN(ohlc4("." + GetSymbol() + AsPrice(DateString) + "P" + AsPrice(strike_minus5))) then 0 else ohlc4("." + GetSymbol() + AsPrice(DateString) + "P" + AsPrice(strike_minus5));
def putOptionohlc46 = if strikes < 6 then 0 else if IsNaN(ohlc4("." + GetSymbol() + AsPrice(DateString) + "P" + AsPrice(strike_minus6))) then 0 else ohlc4("." + GetSymbol() + AsPrice(DateString) + "P" + AsPrice(strike_minus6));
def putOptionohlc47 = if strikes < 7 then 0 else if IsNaN(ohlc4("." + GetSymbol() + AsPrice(DateString) + "P" + AsPrice(strike_minus7))) then 0 else ohlc4("." + GetSymbol() + AsPrice(DateString) + "P" + AsPrice(strike_minus7));
def putOptionohlc48 = if strikes < 8 then 0 else if IsNaN(ohlc4("." + GetSymbol() + AsPrice(DateString) + "P" + AsPrice(strike_minus8))) then 0 else ohlc4("." + GetSymbol() + AsPrice(DateString) + "P" + AsPrice(strike_minus8));
def putOptionohlc49 =if strikes < 9 then 0 else  if IsNaN(ohlc4("." + GetSymbol() + AsPrice(DateString) + "P" + AsPrice(strike_minus9))) then 0 else ohlc4("." + GetSymbol() + AsPrice(DateString) + "P" + AsPrice(strike_minus9));
def putOptionohlc410 = if strikes < 10 then 0 else if IsNaN(ohlc4("." + GetSymbol() + AsPrice(DateString) + "P" + AsPrice(strike_minus10))) then 0 else ohlc4("." + GetSymbol() + AsPrice(DateString) + "P" + AsPrice(strike_minus10));
def putOptionohlc411 = if strikes < 11 then 0 else if IsNaN(ohlc4("." + GetSymbol() + AsPrice(DateString) + "P" + AsPrice(strike_minus11))) then 0 else ohlc4("." + GetSymbol() + AsPrice(DateString) + "P" + AsPrice(strike_minus11));
def putOptionohlc412 = if strikes < 12 then 0 else if IsNaN(ohlc4("." + GetSymbol() + AsPrice(DateString) + "P" + AsPrice(strike_minus12))) then 0 else ohlc4("." + GetSymbol() + AsPrice(DateString) + "P" + AsPrice(strike_minus12));
def putOptionohlc413 = if strikes < 13 then 0 else if IsNaN(ohlc4("." + GetSymbol() + AsPrice(DateString) + "P" + AsPrice(strike_minus13))) then 0 else ohlc4("." + GetSymbol() + AsPrice(DateString) + "P" + AsPrice(strike_minus13));
def putOptionohlc414 = if strikes < 14 then 0 else if IsNaN(ohlc4("." + GetSymbol() + AsPrice(DateString) + "P" + AsPrice(strike_minus14))) then 0 else ohlc4("." + GetSymbol() + AsPrice(DateString) + "P" + AsPrice(strike_minus14));
def putOptionohlc415 = if strikes < 15 then 0 else if IsNaN(ohlc4("." + GetSymbol() + AsPrice(DateString) + "P" + AsPrice(strike_minus15))) then 0 else ohlc4("." + GetSymbol() + AsPrice(DateString) + "P" + AsPrice(strike_minus15));
def putOptionohlc416 = if strikes < 16 then 0 else if IsNaN(ohlc4("." + GetSymbol() + AsPrice(DateString) + "P" + AsPrice(strike_minus16))) then 0 else ohlc4("." + GetSymbol() + AsPrice(DateString) + "P" + AsPrice(strike_minus16));
def putOptionohlc417 = if strikes < 17 then 0 else if IsNaN(ohlc4("." + GetSymbol() + AsPrice(DateString) + "P" + AsPrice(strike_minus17))) then 0 else ohlc4("." + GetSymbol() + AsPrice(DateString) + "P" + AsPrice(strike_minus17));
def putOptionohlc418 = if strikes < 18 then 0 else if IsNaN(ohlc4("." + GetSymbol() + AsPrice(DateString) + "P" + AsPrice(strike_minus18))) then 0 else ohlc4("." + GetSymbol() + AsPrice(DateString) + "P" + AsPrice(strike_minus18));
def putOptionohlc419 = if strikes < 19 then 0 else if IsNaN(ohlc4("." + GetSymbol() + AsPrice(DateString) + "P" + AsPrice(strike_minus19))) then 0 else ohlc4("." + GetSymbol() + AsPrice(DateString) + "P" + AsPrice(strike_minus19));
def putOptionohlc420 = if strikes < 20 then 0 else if IsNaN(ohlc4("." + GetSymbol() + AsPrice(DateString) + "P" + AsPrice(strike_minus20))) then 0 else ohlc4("." + GetSymbol() + AsPrice(DateString) + "P" + AsPrice(strike_minus20));

def putOptionohlc41a = if strikes < 1 then 0 else if IsNaN(ohlc4("." + GetSymbol() + AsPrice(DateString) + "P" + AsPrice(strike_plus1))) then 0 else ohlc4("." + GetSymbol() + AsPrice(DateString) + "P" + AsPrice(strike_plus1));
def putOptionohlc42a = if strikes < 2 then 0 else if IsNaN(ohlc4("." + GetSymbol() + AsPrice(DateString) + "P" + AsPrice(strike_plus2))) then 0 else ohlc4("." + GetSymbol() + AsPrice(DateString) + "P" + AsPrice(strike_plus2));
def putOptionohlc43a = if strikes < 3 then 0 else if IsNaN(ohlc4("." + GetSymbol() + AsPrice(DateString) + "P" + AsPrice(strike_plus3))) then 0 else ohlc4("." + GetSymbol() + AsPrice(DateString) + "P" + AsPrice(strike_plus3));
def putOptionohlc44a = if strikes < 4 then 0 else if IsNaN(ohlc4("." + GetSymbol() + AsPrice(DateString) + "P" + AsPrice(strike_plus4))) then 0 else ohlc4("." + GetSymbol() + AsPrice(DateString) + "P" + AsPrice(strike_plus4));
def putOptionohlc45a = if strikes < 5 then 0 else if IsNaN(ohlc4("." + GetSymbol() + AsPrice(DateString) + "P" + AsPrice(strike_plus5))) then 0 else ohlc4("." + GetSymbol() + AsPrice(DateString) + "P" + AsPrice(strike_plus5));
def putOptionohlc46a = if strikes < 6 then 0 else if IsNaN(ohlc4("." + GetSymbol() + AsPrice(DateString) + "P" + AsPrice(strike_plus6))) then 0 else ohlc4("." + GetSymbol() + AsPrice(DateString) + "P" + AsPrice(strike_plus6));
def putOptionohlc47a = if strikes < 7 then 0 else if IsNaN(ohlc4("." + GetSymbol() + AsPrice(DateString) + "P" + AsPrice(strike_plus7))) then 0 else ohlc4("." + GetSymbol() + AsPrice(DateString) + "P" + AsPrice(strike_plus7));
def putOptionohlc48a = if strikes < 8 then 0 else  if IsNaN(ohlc4("." + GetSymbol() + AsPrice(DateString) + "P" + AsPrice(strike_plus8))) then 0 else ohlc4("." + GetSymbol() + AsPrice(DateString) + "P" + AsPrice(strike_plus8));
def putOptionohlc49a = if strikes < 9 then 0 else if IsNaN(ohlc4("." + GetSymbol() + AsPrice(DateString) + "P" + AsPrice(strike_plus9))) then 0 else ohlc4("." + GetSymbol() + AsPrice(DateString) + "P" + AsPrice(strike_plus9));
def putOptionohlc410a = if strikes < 10 then 0 else if IsNaN(ohlc4("." + GetSymbol() + AsPrice(DateString) + "P" + AsPrice(strike_plus10))) then 0 else ohlc4("." + GetSymbol() + AsPrice(DateString) + "P" + AsPrice(strike_plus10));
def putOptionohlc411a = if strikes < 11 then 0 else if IsNaN(ohlc4("." + GetSymbol() + AsPrice(DateString) + "P" + AsPrice(strike_plus11))) then 0 else ohlc4("." + GetSymbol() + AsPrice(DateString) + "P" + AsPrice(strike_plus11));
def putOptionohlc412a = if strikes < 12 then 0 else if IsNaN(ohlc4("." + GetSymbol() + AsPrice(DateString) + "P" + AsPrice(strike_plus12))) then 0 else ohlc4("." + GetSymbol() + AsPrice(DateString) + "P" + AsPrice(strike_plus12));
def putOptionohlc413a = if strikes < 13 then 0 else if IsNaN(ohlc4("." + GetSymbol() + AsPrice(DateString) + "P" + AsPrice(strike_plus13))) then 0 else ohlc4("." + GetSymbol() + AsPrice(DateString) + "P" + AsPrice(strike_plus13));
def putOptionohlc414a = if strikes < 14 then 0 else if IsNaN(ohlc4("." + GetSymbol() + AsPrice(DateString) + "P" + AsPrice(strike_plus14))) then 0 else ohlc4("." + GetSymbol() + AsPrice(DateString) + "P" + AsPrice(strike_plus14));
def putOptionohlc415a = if strikes < 15 then 0 else if IsNaN(ohlc4("." + GetSymbol() + AsPrice(DateString) + "P" + AsPrice(strike_plus15))) then 0 else ohlc4("." + GetSymbol() + AsPrice(DateString) + "P" + AsPrice(strike_plus15));
def putOptionohlc416a = if strikes < 16 then 0 else if IsNaN(ohlc4("." + GetSymbol() + AsPrice(DateString) + "P" + AsPrice(strike_plus16))) then 0 else ohlc4("." + GetSymbol() + AsPrice(DateString) + "P" + AsPrice(strike_plus16));
def putOptionohlc417a = if strikes < 17 then 0 else if IsNaN(ohlc4("." + GetSymbol() + AsPrice(DateString) + "P" + AsPrice(strike_plus17))) then 0 else ohlc4("." + GetSymbol() + AsPrice(DateString) + "P" + AsPrice(strike_plus17));
def putOptionohlc418a = if strikes < 18 then 0 else if IsNaN(ohlc4("." + GetSymbol() + AsPrice(DateString) + "P" + AsPrice(strike_plus18))) then 0 else ohlc4("." + GetSymbol() + AsPrice(DateString) + "P" + AsPrice(strike_plus18));
def putOptionohlc419a = if strikes < 19 then 0 else if IsNaN(ohlc4("." + GetSymbol() + AsPrice(DateString) + "P" + AsPrice(strike_plus19))) then 0 else ohlc4("." + GetSymbol() + AsPrice(DateString) + "P" + AsPrice(strike_plus19));
def putOptionohlc420a = if strikes < 20 then 0 else if IsNaN(ohlc4("." + GetSymbol() + AsPrice(DateString) + "P" + AsPrice(strike_plus20))) then 0 else ohlc4("." + GetSymbol() + AsPrice(DateString) + "P" + AsPrice(strike_plus20));


####Call Option ohlc4
def callOptionohlc4 = if IsNaN(ohlc4("." + GetSymbol() + AsPrice(DateString) + "C" + AsPrice(strike_base))) then 0 else ohlc4("." + GetSymbol() + AsPrice(DateString) + "C" + AsPrice(strike_base));
def callOptionohlc41 = if strikes < 1 then 0 else if IsNaN(ohlc4("." + GetSymbol() + AsPrice(DateString) + "C" + AsPrice(strike_plus1))) then 0 else ohlc4("." + GetSymbol() + AsPrice(DateString) + "C" + AsPrice(strike_plus1));
def callOptionohlc42 = if strikes < 2 then 0 else if IsNaN(ohlc4("." + GetSymbol() + AsPrice(DateString) + "C" + AsPrice(strike_plus2))) then 0 else ohlc4("." + GetSymbol() + AsPrice(DateString) + "C" + AsPrice(strike_plus2));
def callOptionohlc43 = if strikes < 3 then 0 else if IsNaN(ohlc4("." + GetSymbol() + AsPrice(DateString) + "C" + AsPrice(strike_plus3))) then 0 else ohlc4("." + GetSymbol() + AsPrice(DateString) + "C" + AsPrice(strike_plus3));
def callOptionohlc44 = if strikes < 4 then 0 else if IsNaN(ohlc4("." + GetSymbol() + AsPrice(DateString) + "C" + AsPrice(strike_plus4))) then 0 else ohlc4("." + GetSymbol() + AsPrice(DateString) + "C" + AsPrice(strike_plus4));
def callOptionohlc45 = if strikes < 5 then 0 else if IsNaN(ohlc4("." + GetSymbol() + AsPrice(DateString) + "C" + AsPrice(strike_plus5))) then 0 else ohlc4("." + GetSymbol() + AsPrice(DateString) + "C" + AsPrice(strike_plus5));
def callOptionohlc46 = if strikes < 6 then 0 else if IsNaN(ohlc4("." + GetSymbol() + AsPrice(DateString) + "C" + AsPrice(strike_plus6))) then 0 else ohlc4("." + GetSymbol() + AsPrice(DateString) + "C" + AsPrice(strike_plus6));
def callOptionohlc47 = if strikes < 7 then 0 else if IsNaN(ohlc4("." + GetSymbol() + AsPrice(DateString) + "C" + AsPrice(strike_plus7))) then 0 else ohlc4("." + GetSymbol() + AsPrice(DateString) + "C" + AsPrice(strike_plus7));
def callOptionohlc48 = if strikes < 8 then 0 else if IsNaN(ohlc4("." + GetSymbol() + AsPrice(DateString) + "C" + AsPrice(strike_plus8))) then 0 else ohlc4("." + GetSymbol() + AsPrice(DateString) + "C" + AsPrice(strike_plus8));
def callOptionohlc49 = if strikes < 9 then 0 else if IsNaN(ohlc4("." + GetSymbol() + AsPrice(DateString) + "C" + AsPrice(strike_plus9))) then 0 else ohlc4("." + GetSymbol() + AsPrice(DateString) + "C" + AsPrice(strike_plus9));
def callOptionohlc410 = if strikes < 10 then 0 else if IsNaN(ohlc4("." + GetSymbol() + AsPrice(DateString) + "C" + AsPrice(strike_plus10))) then 0 else ohlc4("." + GetSymbol() + AsPrice(DateString) + "C" + AsPrice(strike_plus10));
def callOptionohlc411 = if strikes < 11 then 0 else if IsNaN(ohlc4("." + GetSymbol() + AsPrice(DateString) + "C" + AsPrice(strike_plus11))) then 0 else ohlc4("." + GetSymbol() + AsPrice(DateString) + "C" + AsPrice(strike_plus11));
def callOptionohlc412 = if strikes < 12 then 0 else if IsNaN(ohlc4("." + GetSymbol() + AsPrice(DateString) + "C" + AsPrice(strike_plus12))) then 0 else ohlc4("." + GetSymbol() + AsPrice(DateString) + "C" + AsPrice(strike_plus12));
def callOptionohlc413 = if strikes < 13 then 0 else if IsNaN(ohlc4("." + GetSymbol() + AsPrice(DateString) + "C" + AsPrice(strike_plus13))) then 0 else ohlc4("." + GetSymbol() + AsPrice(DateString) + "C" + AsPrice(strike_plus13));
def callOptionohlc414 = if strikes < 14 then 0 else if IsNaN(ohlc4("." + GetSymbol() + AsPrice(DateString) + "C" + AsPrice(strike_plus14))) then 0 else ohlc4("." + GetSymbol() + AsPrice(DateString) + "C" + AsPrice(strike_plus14));
def callOptionohlc415 = if strikes < 15 then 0 else if IsNaN(ohlc4("." + GetSymbol() + AsPrice(DateString) + "C" + AsPrice(strike_plus15))) then 0 else ohlc4("." + GetSymbol() + AsPrice(DateString) + "C" + AsPrice(strike_plus15));
def callOptionohlc416 = if strikes < 16 then 0 else if IsNaN(ohlc4("." + GetSymbol() + AsPrice(DateString) + "C" + AsPrice(strike_plus16))) then 0 else ohlc4("." + GetSymbol() + AsPrice(DateString) + "C" + AsPrice(strike_plus16));
def callOptionohlc417 = if strikes < 17 then 0 else if IsNaN(ohlc4("." + GetSymbol() + AsPrice(DateString) + "C" + AsPrice(strike_plus17))) then 0 else ohlc4("." + GetSymbol() + AsPrice(DateString) + "C" + AsPrice(strike_plus17));
def callOptionohlc418 = if strikes < 18 then 0 else if IsNaN(ohlc4("." + GetSymbol() + AsPrice(DateString) + "C" + AsPrice(strike_plus18))) then 0 else ohlc4("." + GetSymbol() + AsPrice(DateString) + "C" + AsPrice(strike_plus18));
def callOptionohlc419 = if strikes < 19 then 0 else if IsNaN(ohlc4("." + GetSymbol() + AsPrice(DateString) + "C" + AsPrice(strike_plus19))) then 0 else ohlc4("." + GetSymbol() + AsPrice(DateString) + "C" + AsPrice(strike_plus19));
def callOptionohlc420 = if strikes < 20 then 0 else if IsNaN(ohlc4("." + GetSymbol() + AsPrice(DateString) + "C" + AsPrice(strike_plus20))) then 0 else ohlc4("." + GetSymbol() + AsPrice(DateString) + "C" + AsPrice(strike_plus20));

def callOptionohlc41a = if strikes < 1 then 0 else if IsNaN(ohlc4("." + GetSymbol() + AsPrice(DateString) + "C" + AsPrice(strike_minus1))) then 0 else ohlc4("." + GetSymbol() + AsPrice(DateString) + "C" + AsPrice(strike_minus1));
def callOptionohlc42a = if strikes < 2 then 0 else if IsNaN(ohlc4("." + GetSymbol() + AsPrice(DateString) + "C" + AsPrice(strike_minus2))) then 0 else ohlc4("." + GetSymbol() + AsPrice(DateString) + "C" + AsPrice(strike_minus2));
def callOptionohlc43a = if strikes < 3 then 0 else if IsNaN(ohlc4("." + GetSymbol() + AsPrice(DateString) + "C" + AsPrice(strike_minus3))) then 0 else ohlc4("." + GetSymbol() + AsPrice(DateString) + "C" + AsPrice(strike_minus3));
def callOptionohlc44a = if strikes < 4 then 0 else if IsNaN(ohlc4("." + GetSymbol() + AsPrice(DateString) + "C" + AsPrice(strike_minus4))) then 0 else ohlc4("." + GetSymbol() + AsPrice(DateString) + "C" + AsPrice(strike_minus4));
def callOptionohlc45a = if strikes < 5 then 0 else if IsNaN(ohlc4("." + GetSymbol() + AsPrice(DateString) + "C" + AsPrice(strike_minus5))) then 0 else ohlc4("." + GetSymbol() + AsPrice(DateString) + "C" + AsPrice(strike_minus5));
def callOptionohlc46a = if strikes < 6 then 0 else if IsNaN(ohlc4("." + GetSymbol() + AsPrice(DateString) + "C" + AsPrice(strike_minus6))) then 0 else ohlc4("." + GetSymbol() + AsPrice(DateString) + "C" + AsPrice(strike_minus6));
def callOptionohlc47a = if strikes < 7 then 0 else if IsNaN(ohlc4("." + GetSymbol() + AsPrice(DateString) + "C" + AsPrice(strike_minus7))) then 0 else ohlc4("." + GetSymbol() + AsPrice(DateString) + "C" + AsPrice(strike_minus7));
def callOptionohlc48a = if strikes < 8 then 0 else if IsNaN(ohlc4("." + GetSymbol() + AsPrice(DateString) + "C" + AsPrice(strike_minus8))) then 0 else ohlc4("." + GetSymbol() + AsPrice(DateString) + "C" + AsPrice(strike_minus8));
def callOptionohlc49a = if strikes < 9 then 0 else if IsNaN(ohlc4("." + GetSymbol() + AsPrice(DateString) + "C" + AsPrice(strike_minus9))) then 0 else ohlc4("." + GetSymbol() + AsPrice(DateString) + "C" + AsPrice(strike_minus9));
def callOptionohlc410a = if strikes < 10 then 0 else if IsNaN(ohlc4("." + GetSymbol() + AsPrice(DateString) + "C" + AsPrice(strike_minus10))) then 0 else ohlc4("." + GetSymbol() + AsPrice(DateString) + "C" + AsPrice(strike_minus10));
def callOptionohlc411a = if strikes < 11 then 0 else if IsNaN(ohlc4("." + GetSymbol() + AsPrice(DateString) + "C" + AsPrice(strike_minus11))) then 0 else ohlc4("." + GetSymbol() + AsPrice(DateString) + "C" + AsPrice(strike_minus11));
def callOptionohlc412a = if strikes < 12 then 0 else if IsNaN(ohlc4("." + GetSymbol() + AsPrice(DateString) + "C" + AsPrice(strike_minus12))) then 0 else ohlc4("." + GetSymbol() + AsPrice(DateString) + "C" + AsPrice(strike_minus12));
def callOptionohlc413a = if strikes < 13 then 0 else if IsNaN(ohlc4("." + GetSymbol() + AsPrice(DateString) + "C" + AsPrice(strike_minus13))) then 0 else ohlc4("." + GetSymbol() + AsPrice(DateString) + "C" + AsPrice(strike_minus13));
def callOptionohlc414a = if strikes < 14 then 0 else if IsNaN(ohlc4("." + GetSymbol() + AsPrice(DateString) + "C" + AsPrice(strike_minus14))) then 0 else ohlc4("." + GetSymbol() + AsPrice(DateString) + "C" + AsPrice(strike_minus14));
def callOptionohlc415a = if strikes < 15 then 0 else if IsNaN(ohlc4("." + GetSymbol() + AsPrice(DateString) + "C" + AsPrice(strike_minus15))) then 0 else ohlc4("." + GetSymbol() + AsPrice(DateString) + "C" + AsPrice(strike_minus15));
def callOptionohlc416a = if strikes < 16 then 0 else if IsNaN(ohlc4("." + GetSymbol() + AsPrice(DateString) + "C" + AsPrice(strike_minus16))) then 0 else ohlc4("." + GetSymbol() + AsPrice(DateString) + "C" + AsPrice(strike_minus16));
def callOptionohlc417a = if strikes < 17 then 0 else if IsNaN(ohlc4("." + GetSymbol() + AsPrice(DateString) + "C" + AsPrice(strike_minus17))) then 0 else ohlc4("." + GetSymbol() + AsPrice(DateString) + "C" + AsPrice(strike_minus17));
def callOptionohlc418a = if strikes < 18 then 0 else if IsNaN(ohlc4("." + GetSymbol() + AsPrice(DateString) + "C" + AsPrice(strike_minus18))) then 0 else ohlc4("." + GetSymbol() + AsPrice(DateString) + "C" + AsPrice(strike_minus18));
def callOptionohlc419a = if strikes < 19 then 0 else if IsNaN(ohlc4("." + GetSymbol() + AsPrice(DateString) + "C" + AsPrice(strike_minus19))) then 0 else ohlc4("." + GetSymbol() + AsPrice(DateString) + "C" + AsPrice(strike_minus19));
def callOptionohlc420a = if strikes < 20 then 0 else if IsNaN(ohlc4("." + GetSymbol() + AsPrice(DateString) + "C" + AsPrice(strike_minus20))) then 0 else ohlc4("." + GetSymbol() + AsPrice(DateString) + "C" + AsPrice(strike_minus20));


def totalcall_prem = (callOptionVolume * callOptionohlc4) + (callOptionVolume1 * callOptionohlc41) + (callOptionVolume2 * callOptionohlc42) + (callOptionVolume3 * callOptionohlc43) + (callOptionVolume4 * callOptionohlc44) + (callOptionVolume5 * callOptionohlc45) + (callOptionVolume6 * callOptionohlc46) + (callOptionVolume7 * callOptionohlc47) + (callOptionVolume8 * callOptionohlc48) + (callOptionVolume9 * callOptionohlc49) + (callOptionVolume10 * callOptionohlc410) + (callOptionVolume11 * callOptionohlc411) + (callOptionVolume12 * callOptionohlc412) + (callOptionVolume13 * callOptionohlc413) + (callOptionVolume14 * callOptionohlc414) + (callOptionVolume15 * callOptionohlc415) + (callOptionVolume16 * callOptionohlc416) + (callOptionVolume17 * callOptionohlc417) + (callOptionVolume18 * callOptionohlc418) + (callOptionVolume19 * callOptionohlc419) + (callOptionVolume20 * callOptionohlc420) + (callOptionVolume1a * callOptionohlc41a) + (callOptionVolume2a * callOptionohlc42a) + (callOptionVolume3a * callOptionohlc43a) + (callOptionVolume4a * callOptionohlc44a) + (callOptionVolume5a * callOptionohlc45a) + (callOptionVolume6a * callOptionohlc46a) + (callOptionVolume7a * callOptionohlc47a) + (callOptionVolume8a * callOptionohlc48a) + (callOptionVolume9a * callOptionohlc49a) + (callOptionVolume10a * callOptionohlc410a) + (callOptionVolume11a * callOptionohlc411a) + (callOptionVolume12a * callOptionohlc412a) + (callOptionVolume13a * callOptionohlc413a) + (callOptionVolume14a * callOptionohlc414a) + (callOptionVolume15a * callOptionohlc415a) + (callOptionVolume16a * callOptionohlc416a) + (callOptionVolume17a * callOptionohlc417a) + (callOptionVolume18a * callOptionohlc418a) + (callOptionVolume19a * callOptionohlc419a) + (callOptionVolume20a * callOptionohlc420a);
def totalput_prem = (putOptionVolume * putOptionohlc4) + (putOptionVolume1 * putOptionohlc41) + (putOptionVolume2 * putOptionohlc42) + (putOptionVolume3 * putOptionohlc43) + (putOptionVolume4 * putOptionohlc44) + (putOptionVolume5 * putOptionohlc45) + (putOptionVolume6 * putOptionohlc46) + (putOptionVolume7 * putOptionohlc47) + (putOptionVolume8 * putOptionohlc48) + (putOptionVolume9 * putOptionohlc49) + (putOptionVolume10 * putOptionohlc410) + (putOptionVolume11 * putOptionohlc411) + (putOptionVolume12 * putOptionohlc412) + (putOptionVolume13 * putOptionohlc413) + (putOptionVolume14 * putOptionohlc414) + (putOptionVolume15 * putOptionohlc415) + (putOptionVolume16 * putOptionohlc416) + (putOptionVolume17 * putOptionohlc417) + (putOptionVolume18 * putOptionohlc418) + (putOptionVolume19 * putOptionohlc419) + (putOptionVolume20 * putOptionohlc420) + (putOptionVolume1a * putOptionohlc41a) + (putOptionVolume2a * putOptionohlc42a) + (putOptionVolume3a * putOptionohlc43a) + (putOptionVolume4a * putOptionohlc44a) + (putOptionVolume5a * putOptionohlc45a) + (putOptionVolume6a * putOptionohlc46a) + (putOptionVolume7a * putOptionohlc47a) + (putOptionVolume8a * putOptionohlc48a) + (putOptionVolume9a * putOptionohlc49a) + (putOptionVolume10a * putOptionohlc410a) + (putOptionVolume11a * putOptionohlc411a) + (putOptionVolume12a * putOptionohlc412a) + (putOptionVolume13a * putOptionohlc413a) + (putOptionVolume14a * putOptionohlc414a) + (putOptionVolume15a * putOptionohlc415a) + (putOptionVolume16a * putOptionohlc416a) + (putOptionVolume17a * putOptionohlc417a) + (putOptionVolume18a * putOptionohlc418a) + (putOptionVolume19a * putOptionohlc419a) + (putOptionVolume20a * putOptionohlc420a);

plot put_prem = totalput_prem*100;
put_prem.SetDefaultColor(Color.RED);
put_prem.SetStyle(Curve.FIRM);

plot call_prem = totalcall_prem*100;
call_prem.SetDefaultColor(Color.GREEN);
call_prem.SetStyle(Curve.FIRM);



#def cumulative_calls_minus_puts =  totalcalls_puts + totalcalls_puts[1];
#AddLabel(yes, "Cumulative_Premium1: $" + cumulative_calls_minus_puts);
#AddLabel(yes, "Cumulative_Premium: $" + TotalSum(cumulative_calls_minus_puts));
#AddLabel(yes, "Total Calls: $" + TotalSum(totalcalls_today), 
