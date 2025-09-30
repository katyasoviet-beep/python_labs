prise=int(input('Цена:'))
discount=int(input('Скидка(%):'))
vat=int(input('НДС(%):'))
base=prise*(1-discount/100)
vat_amount = base * (vat/100)
total = base + vat_amount
print('База после скидки:', base)
print('НДС:', vat_amount)
print('Итого к оплате:', total)
