# TIG054_projekt

Moduler som krävs:
PyQt5
detectlanguage
googletrans

Funktionalitet som hämtas utifrån: Språkdetektering från detectlanguage.com (API), översättning genom Google Translate, med modulen googletrans

Detta är ett översättningsprogram med följande funktionalitet:
- Öppna filer från hårddisken och hämta innehållet, eller skriv in egen text
- Detektera språk
- Översätt text som en helhet med bevarad grammatik
- Skapa ordlista: Översätter valda ord, ord för ord, utan bevarad grammatik och skapar en liten ordlista bestående av max 10 ord med orden på originalspråk + översättning. Ett gränsvärde är satt för att inte överstiga begränsning i mängd data för googletrans. Finns fler än tio ord i användarens text så slumpas 10 ord från texten.
- Spara fil, låter användaren spara sin skapta ordlista som en textfil på hårddisken

Användning:
1) Är ingen databas skapad måste användaren först skapa och fylla databasen genom att köra filen fa_db_functionality.py
2) Finns en databas redan så hoppas steg 1 över
3) Sedan ska alla andra moduler fungera
4) Skriv in text i den översta textrutan eller tryck på 'hämta textfil' för att navigera till en fil att öppna hårddisken
5) Justera vilken typ av frekvensanalys du vill använda med reglaget. Antingen egen frekvensanalys (mer inexakt) eller användning av frekvensanalys via detectlanguage.com (hämtas via API och har en databegränsning)
6) Använd rullgardinsmenyn för att välja ett språk att översätta till
7) Klicka på översätt för att översätta hela texten med bevarad grammatik
8) Klicka på skapa ordlista för att skapa en ordlista av tio ord (slumpmässigt om din text består av mer än tio ord)
9) Klicka på spara ordlista som textfil för att spara din ordlista som en textfil på hårddisken
10) Klicka på rensa för att nollställa det du skrivit in och eventuella ordlistor och översättningar som skapats



![Skärmavbild 2020-03-22 kl  22 55 21](https://user-images.githubusercontent.com/56775140/77261645-4233c180-6c90-11ea-8363-1d056603f2c3.png)

