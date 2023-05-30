#!/bin/bash
# bash script.sh
# no pip install required

declare -a POSSIBLE_CURRENCIES=("AUD" "BGN" "CAD" "CHF" "CZK" "DKK" "EUR" "GBP" "HUF" "INR" "JPY" "NOK" "NZD" "PLN" "RON" "RUB" "SEK" "SGD" "USD")

targetCurrency=USD

#profileContry=US
profileContry=GB

for c in "${POSSIBLE_CURRENCIES[@]}"; do
  sourceCurrency=$c
  tmp_file=tmp/${sourceCurrency}_${targetCurrency}.json

  curl "https://wise.com/gateway/v1/price?sourceCurrency=${sourceCurrency}&targetCurrency=${targetCurrency}&profileCountry=${profileConuntry}&markers=FCF_PRICING&profileType=PERSONAL&targetAmount=1000" > $tmp_file
done

for c in "${POSSIBLE_CURRENCIES[@]}"; do
  sourceCurrency=$c
  tmp_file=tmp/${sourceCurrency}_${targetCurrency}.json

  cat $tmp_file | jq -c '.[] | select(.payInMethod == "VISA_CREDIT" and .payOutMethod == "BALANCE") | .sourceCcy +" "+ (.variableFeePercent|tostring) +"% "+  (.variableFee|tostring) +" "+ (.total|tostring)'
done
