import math as mt
import pandas as pd
import random
import sys
random.seed()

class Int_Alias:
    def __init__(self, str):
        self.val = random.randrange(979579579, sys.maxsize)
        self.str = str

    def apply(self, str = None):
        if str == None or str == self.str:
            return self.val
        else:
            return str

    def decrypt(self, inpt):
        return inpt.replace(str(self.val), self.str)

    def getVal(self):
        return self.val

    def getStr(self):
        return self.str

def invertArray(col_arr):
    res = [[] for i in range(len(col_arr[0]))]
    for c in range(len(col_arr)):
        for r in range(len(col_arr[0])):
            res[r].append(col_arr[c][r])
    return res


def getCommaIndex(inpt_str):
    commaInd_inpt = -1
    for i in range(len(inpt_str)):
        commaInd_inpt = i if inpt_str[i] == '.' else commaInd_inpt
    if commaInd_inpt ==-1:
        commaInd_inpt = len(inpt_str) - 1
    return commaInd_inpt

def sig_format(inpt, err, sig_dgts, smallDigits = True):
    pot = 0
    if smallDigits and (np.abs(inpt) < 10**(-3) or np.abs(err) < 10**(-3)):
        pot = mt.ceil(np.max([0, -mt.log10(np.abs(inpt)) if inpt != 0 else 0, -mt.log10(np.abs(err)) if err != 0 else 0]))
        inpt *= 10**pot
        err *= 10**pot
    err_str = str(err)
    isSig = False
    lastSigInd = 0
    sigToGo = sig_dgts
    commaInd = -1
    for i in range(len(err_str)):
        if isSig == False and not err_str[i] in ['0', '.']:
            isSig = True
            if err_str[i] in ['1', '2'] and sig_dgts == 1:
                sigToGo += 1

        if err_str[i] == '.':
            commaInd = i
        else:
            sigToGo -= isSig
        if sigToGo > 0:
            lastSigInd += 1

    if sigToGo > 0:
        sig_dgts -= 1
        lastSigInd -= 1
    if commaInd == -1:
        commaInd = len(err_str)
    commaInd = commaInd if commaInd != -1 else len(err_str)
    dec_pot = - lastSigInd + commaInd - (lastSigInd < commaInd)
    err = err * 10**(-dec_pot)
    err = mt.ceil(err)
    err_str = str(err * 10**(dec_pot))
    if lastSigInd > commaInd:
        err_str = err_str[:lastSigInd + 1]

    inpt *= 10**(-dec_pot)
    inpt_str = str(round(inpt) * 10**dec_pot)
    commaInd_inpt = getCommaIndex(inpt_str)

    if len(inpt_str) - 1 - commaInd_inpt != -dec_pot:
        inpt_str += '0'
    commaInd_inpt = getCommaIndex(inpt_str)


    inpt_str = inpt_str[:commaInd_inpt - dec_pot + 1]
    if commaInd_inpt - dec_pot + 1 < commaInd_inpt:
        inpt_str += " \cdot 10^{" + str(dec_pot - 1) +"}"
    inpt_str = inpt_str

    if pot != 0:
        inpt_str += ("\cdot 10^{" + str(-pot) + "}" if pot != 0 else "")
        err_str += ("\cdot 10^{" + str(-pot) + "}" if pot != 0 else "")
    return inpt_str, err_str


def isNumber(obj):
    try:
        tmp = int(obj)
        return True
    except:
        return False
#IMPORTANT NOTE: CANT HANDLE SIGNIFICANT 0 AS LAST DIGIT! (for example error 0.10 will be treated as 0.1)

def sigFormatTable(arr, val_err_indices, sig_digits = 1, int_cols = [], debug = False):
    res = [["undefined" for k in range(len(arr[i]))] for i in range(len(arr))]
    trashCan = []
    for i in range(len(arr)):
        for j in val_err_indices:
            if i == j[0]:
                for k in range(len(arr[i])):
                    if not isNumber(arr[i][k]):
                        res[i][k] = str(arr[i][k])
                        if debug:
                            print(res[i][k])
                        continue
                    fmt = sig_format(arr[i][k], arr[j[1]][k], sig_digits)
                    res[i][k] =  "$ " + fmt[0] + " \pm " + fmt[1]
                    if arr[i][k] != 0:
                        res[i][k] += "\: (\pm " + sig_format(0, np.abs(100.0 * arr[j[1]][k]/arr[i][k]), 2, smallDigits=False)[1] + "\%)"
                    res[i][k] += "$"
                trashCan.append(j[1])
                break
        if res[i][0] == "undefined":
            for k in range(len(arr[i])):
                if not isNumber(arr[i][k]):
                    res[i][k] = str(arr[i][k])
                    continue
                if i in int_cols:
                   res[i][k] = "$ " + str(int(arr[i][k])) + "$"
                else:
                    res[i][k] = "$ " + sig_format(arr[i][k], arr[i][k], sig_digits)[0] + "$"


    for e in trashCan:
        res.pop(e)
        for i in range(len(trashCan)):
            if trashCan[i] > e:
                trashCan[i] = trashCan[i] - 1
    return res

#IMPORTANT NOTE: CANT HANDLE SIGNIFICANT 0 AS LAST DIGIT! (for example error 0.10 will be treated as 0.1)

def asLatex(arr, col_labels, dontInvert = False):
    df = pd.DataFrame(invertArray(arr), columns=col_labels) if not dontInvert else pd.DataFrame(arr, columns = col_labels)
    cformate = "|"
    for i in df.columns:
        cformate += "l|"

    res = """\\begin{table}[]\n
    \t\centering\n
    \t\caption{CHANGE THIS LATER}\n\t""" + df.style.hide(axis="index").to_latex(column_format=cformate, hrules = True).replace("toprule", "hline").replace("\n", "\n\t\t") + "\t\label{tab:my_label}\n" + "\end{table}"
    res = res.replace("midrule", "hline")
    return res.replace("bottomrule", "hline")

def printTable(arr, col_labels):
    df = pd.DataFrame(invertArray(arr), columns=col_labels)
    print(df.to_markdown())

def showTable(arr, col_labels):
    df = pd.DataFrame(invertArray(arr), columns=col_labels)
    display(df)

def weightedMiddle(arr, err_arr):
    val = 0
    err = 0
    for i in range(len(arr)):
        val += arr[i]/err_arr[i]**2
        err += 1/err_arr[i]**2

    return val/err, np.sqrt(1/err)

def indexOf(arr):
    return range(len(arr))

class Fit:
    def __init__(self, slope, intercept, sigSlope, sigIntercept, chiSquared):
        self.slope = slope
        self.intercept = intercept
        self.sigSlope = sigSlope
        self.sigIntercept = sigIntercept
        self.chiSquared = chiSquared

    def __str__(self):
        res = "$m = " + sig_format(self.slope, self.sigSlope, 1)[0] + "\pm" + sig_format(self.slope, self.sigSlope, 1)[1]
        if self.slope != 0:
            res += "(\pm" + sig_format(0, self.sigSlope/self.slope, 2, smallDigits=False)[1] + "\%)"
        res += "$\n$b = " + sig_format(self.intercept, self.sigIntercept, 1)[0] + "\pm" + sig_format(self.intercept, self.sigIntercept, 1)[1]
        if self.intercept != 0:
            res += "(\pm" + sig_format(0, self.sigIntercept/self.intercept, 2, smallDigits=False)[1] + "\%)"
        res += "$\n$\chi^2 = " + self.chiSquared + "$"
        return res

def linReg(xdata, ydata, yerr = None):
    if yerr == None:
        yerr = [1 for i in ydata]
    if len(xdata) != len(ydata):
        print(" :( Error :( : xdata and ydata are ment to resemble pairs of (x,y)-Values. Thisfor, xdata and ydata need to have the same dimension. Since thats currently not the case, I assume very much, that you messed up. Sorry for that, happy bug-fixing...")
    delta = 0

    oneOverSig2 = 0
    x2overSig2 = 0
    xOverSig2 = 0
    xyOverSig2 = 0
    yOverSig2 = 0
    for i in indexOf(xdata):
        oneOverSig2 += 1/yerr[i]**2
        x2overSig2 += xdata[i]**2/yerr[i]**2
        xOverSig2 += xdata[i]/yerr[i]**2
        xyOverSig2 += xdata[i] * ydata[i]/yerr[i]**2
        yOverSig2 += ydata[i]/yerr[i]**2

    Delta = oneOverSig2 * x2overSig2 - xOverSig2**2
    m = 1/Delta * (oneOverSig2 * xyOverSig2 - xOverSig2 * yOverSig2)
    b = 1/Delta * (x2overSig2 * yOverSig2 - xOverSig2 * xyOverSig2)
    sigM = (1/Delta * oneOverSig2)**(0.5)
    sigB = (1/Delta * x2overSig2)
    chi2 = 0
    for i in indexOf(xdata):
        chi2 += (1/yerr[i] * ydata[i] - m * xdata[i] - b)**2

    return Fit(m, b, sigM, sigB, chi2)

class Set:
    def __init__(self, arr):
        self.asArr = []
        for elem in arr:
            if not elem in self.asArr:
                self.asArr.append(elem)

def printFileAsLatex(path, val_err_index_pairs):
    dat, lbls = load(path)
    print(asLatex(sigFormatTable(dat, val_err_index_pairs), lbls))

def arr_to_csv(arr, lbls, path):
    pd.DataFrame(invertArray(arr)).to_csv(path, sep = ";", index=False, header = lbls)

    def latexSigFormat(val, err, sigDgts=1, relativSigDigits=2, printOut=False, variableName=""):
        res = "$" + variableName + (" = " if variableName != "" else "") + sig_format(val, err, sigDgts)[0] + " \pm " + \
              sig_format(val, err, sigDgts)[1] + " (\pm " + sig_format(138713, 100 * err / val, relativSigDigits)[
                  1] + "\%)$"
        if printOut:
            print(res)

        return res