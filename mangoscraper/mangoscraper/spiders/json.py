import csv

new_list = []

for fn in range(len(a)):
    new_list.append(a[fn]['display_text'])
print(new_list)

with open('food_type.csv', 'w', newline='') as csvfile:
    fieldnames = ['id', 'food_type']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    
    writer.writeheader()

    for index, item in enumerate(new_list):
        writer.writerow({'id':index, 'food_type':item })
        

