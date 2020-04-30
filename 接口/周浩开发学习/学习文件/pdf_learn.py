import pdfplumber
import pandas as pd
import re
path = r'C:\Users\admin\Desktop\AA.pdf'
a = [i for i in range(59)]
with pdfplumber.open(path) as pdf:
    first_page = pdf.pages[0]
    # print(first_page)
    # for table in first_page.extract_tables():
    #     df = pd.DataFrame(table[5:])
    #     print(df)
    #     break
    df = pd.DataFrame(first_page.extract_tables()[0][5:])
    print(df)

        # values = df.values
        # for i in range(0, len(values)):
        #     print(values[i])
        #     if re.search(str(values[i]),'#'):
        #         print('第%s行发现问题值' % i)
        #         break

