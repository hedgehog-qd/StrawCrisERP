import os
import pandas as pd
import db


def processUpdateBOMupdateDB(filename, upload_path):
    data = pd.read_excel(upload_path)
    for i in range(0, len(data)):
        print("dealing with line: " + str(i))
        if db.checkMaterialExists(str(data.iloc[i]['MPN'])) == 1:  # 该条目已经存在
            print("样本 " + str(data.iloc[i]['MPN']) + " 已经存在")
            existing_num = db.getMaterialInfowithMPN(str(data.iloc[i]['MPN']))[4]
            db.updateMaterialQuantitywithMPN(str(data.iloc[i]['MPN']),
                                             int(existing_num) + int(data.iloc[i]['Quantity']))
        else:
            print("样本 " + str(data.iloc[i]['MPN']) + " 是新条目")
            db.addNewMaterial(str(data.iloc[i]['Name']), str(data.iloc[i]['Class']), str(data.iloc[i]['Footprint']),
                              str(data.iloc[i]['Quantity']), str(data.iloc[i]['MPN']), str(data.iloc[i]['Manufacture']),
                              str(data.iloc[i]['SPN']), str(data.iloc[i]['Supplier']), str(data.iloc[i]['Position']),
                              str(data.iloc[i]['Comment']), str(data.iloc[i]['Time']))
    return


def processCompareBOM(filename, upload_path):
    data = pd.read_excel(upload_path)
    whatWeHave = []
    whatWeDontHave = []
    for i in range(0, len(data)):
        print("dealing with line:" + str(i))
        if (len(str(data.iloc[i]['MPN'])) == 0) or (str(data.iloc[i]['MPN']) == "nan"):
            continue
        if db.checkMaterialExists(str(data.iloc[i]['MPN'])) == 0:  # 条目不存在
            print("样本 " + str(data.iloc[i]['MPN']) + " 不存在")
            donthavetemp = []
            donthavetemp.append(str(data.iloc[i]['MPN']))
            donthavetemp.append("Requested: " + str(data.iloc[i]['Quantity']) + ", Have: 0")
            whatWeDontHave.append(donthavetemp)
        elif int(db.getMaterialInfowithMPN(str(data.iloc[i]['MPN']))[4]) < int(data.iloc[i]['Quantity']):  # 库存不足
            print("样本 " + str(data.iloc[i]['MPN']) + " 库存不足")
            donthavetemp = []
            donthavetemp.append(str(data.iloc[i]['MPN']))
            donthavetemp.append("Requested: " + str(data.iloc[i]['Quantity']) + ", Have: " + str(
                db.getMaterialInfowithMPN(str(data.iloc[i]['MPN']))[4]))
            whatWeDontHave.append(donthavetemp)
        else:  # OK
            print("样本 " + str(data.iloc[i]['MPN']) + " 已加入")
            havetemp = []
            havetemp.append(str(data.iloc[i]['MPN']))
            havetemp.append("Requested: " + str(data.iloc[i]['Quantity']) + ", Have: " + str(
                db.getMaterialInfowithMPN(str(data.iloc[i]['MPN']))[4]))
            havetemp.append(str(data.iloc[i]['Quantity']))
            whatWeHave.append(havetemp)
    print("done")
    return whatWeHave, whatWeDontHave
