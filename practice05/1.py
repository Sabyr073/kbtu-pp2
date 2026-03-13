import re
import json    
def ali(raw):
    with open(raw,'r',encoding='utf-8') as file:
        text=file.read()
    date_pattern = r"Время:\s(\d{2}\.\d{2}\.\d{4}\s\d{2}:\d{2}:\d{2})"
    payment_method_pattern = "Банковская карта|Наличные"
    payment_amount_pattern = r"(Банковская карта|Наличные):\s*([\d\s\,]*)\b"
    total_amout_pattern = r"ИТОГО:\s*([\d\s\,]*)\b"
    item_pattern = r"([\d\.]+)\s(.+)\s([\d]+),\d{3}\sx\s(\d+),\d+\s\d+,\d{2}\sСтоимость\s(\d+),\d{2}"
    out1 = (re.search(date_pattern,text)).group(1)
    out2 = (re.search(payment_method_pattern,text)).group()
    out3 = float(((re.search(payment_amount_pattern,text)).group(2)).replace(" ","").replace(",","."))
    out4 = float(((re.search(total_amout_pattern,text)).group(1)).replace(" ","").replace(",","."))
    out5 = re.findall(item_pattern,text)
    output_code = {
        "datetime": out1,
        "payment_method": out2,
        "payment_amount": out3,
        "total_amount": out4,
        "item": []
    }
    for i in range(len(out5)):
        pp={
            "number_of_item": out5[i][0], 
            "name_of_item": out5[i][1],
            "count_of_item": int(out5[i][2]),
            "price_per_item": float(out5[i][3]),
            "total_price": float(out5[i][4])
        }
        output_code["item"].append(pp)       
    return output_code

output_data = ali('raw.txt')
output_json = json.dumps(output_data, indent=4, ensure_ascii=False)
print(output_json)