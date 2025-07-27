واسه ساختن برنچ جدید از تو وی اس کد که راحته و میریم رو پایین که main نوشته و میزنیم create new branch و اسممون رو میدیم
مثلا
feature/products-view
کدش هم اینه
git checkout -b products-view

برای دریافت اخرین تغییرات هم از تو وی اس کد میریم تو خود اون برنچ از پایین و رو برنچ مربوطه وایمیسم و pull رو میزنیم
کد دستیش هم اینه:
git checkout branch-name
git pull origin branch-name

واسه اد کردن و کامیت هم که با وی اس کد راحته 
و کدش میشه این
git add .
git commit -m "commit message"

واسه پوش کردن هم که باز دکمه پوش تو وی اس کد و  کد دستیش:
git push origin branch_name

مرحله اخرم وقتی تغییرات تموم شد میرین داخل گیت هاب و تو صفحه ریپو رو Compare & Pull Request کلیک میکنیم
بعد توضیح میدیم چه کاری کردیم
و درخواست رو میزنیم به dev نه main
حواسمون باشه به main نزنیم
قانون مهم: هیچ‌کس مستقیم روی main یا dev کار نمی‌کنه!
همه فقط روی شاخه‌های feature/... کار می‌کنن و با  Pull Request تغییراتشون رو به dev می‌فرستن.

مرحله بعد هم مرج کردن به main هستش 
که وقتی همه چیز تست شد اینکارو میکنیم:
git checkout main
git merge dev
git push origin main

نکته‌های حرفه‌ای
همیشه قبل از شروع کد:

git checkout dev
git pull origin dev

قبل از Push کردن، مطمئن شو روی شاخه درست هستی:
git branch

حتماً هر کامیت باید معنی‌دار باشه:
git commit -m "Add login form validation"
