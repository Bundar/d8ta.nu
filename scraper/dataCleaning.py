import sys
import csv
import unicodedata

args = sys.argv
print("Working on: " + str(args[1]))
if args[1] == 'routes':
    path = './data/route-data/'
    filename = 'routeData'
    print("Route env set up")
else:
    path = './data/boulder-data/'
    filename = 'boulderData'
    print("Boulder env set up")

def validate_p(p):
    return p
def validate_sc(sc):
    scp = unicodedata.normalize("NFKD", sc).replace(' ', '' )
    return scp
def validate_nm(nm):
    return nm

def validate_dob(dob):
    return dob
def validate_ctr(ctr):
    return ctr
def validate_ht(ht):
    if type(ht) != type(''):
        print("Wrong type")
        return ht
    return ht.strip(' cm')
def validate_wt(wt):
    return wt.strip('about ').strip(' kg')
def validate_strt(strt):
    return strt
def calc_bmi(ht, wt):
    try:
        bmi = int(wt)/(int(ht)/100)**2
    except:
        bmi = ''
    finally:
        return bmi

def main():
    
    i = 0

    while i < 10:
        fromFile = open(path+filename+str(i)+'.csv', 'r', newline='')
        toFile  = open(path+'cleaned-'+filename+str(i)+'.csv', 'w', newline='')

        obj = csv.reader(fromFile, delimiter = ' ', quotechar = '|', quoting = csv.QUOTE_MINIMAL)
        writer = csv.writer(toFile, delimiter = ',', quotechar='"', quoting = csv.QUOTE_MINIMAL)

        c = 0
        for row in obj:
            #print(row)
            if c == 0:
                c+=1
                writer.writerow(['Placeing', 'Score', 'Name', 'Birth Year', 'Country', 'Height (cm)', 'Weight (Kg)', 'Started Climbing', 'Climber BMI'])
                continue
        
            p = row[0]
            sc = row[1]
            nm = row[2]
            dob = row[3]
            ctr = row[4]
            ht = row[5]
            wt = row[6]
            strt = row[7]
        
            p = validate_p(p)
            sc = validate_sc(sc)
            nm = validate_nm(nm)
            dob = validate_dob(dob)
            ctr = validate_ctr(ctr)
            ht = validate_ht(ht)
            wt = validate_wt(wt)
            strt = validate_strt(strt)
            bmi = calc_bmi(ht, wt)
            print(p + ', ' + sc + ', ' + nm + ', ' + dob + ', ' + ctr + ', ' + ht + ', ' + wt + ', ' + strt + ', ' + str(bmi))
            writer.writerow([p, sc, nm, dob, ctr, ht, wt, strt, str(bmi)])
        toFile.close()
        fromFile.close()
        i+=1
if __name__ ==  '__main__':
    main()
