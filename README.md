واسه ساختن برنچ جدید از تو VS Code که راحته و میریم رو پایین که `main‍` نوشته و میزنیم create new branch و اسممون رو میدیم. مثلا `feature/products-view`
کدش هم اینه
```bash
git checkout -b feature/products-view
```
برای دریافت اخرین تغییرات هم از تو VS Code میریم تو خود اون برنچ از پایین و رو برنچ مربوطه وایمیسم و pull رو میزنیم.
کد دستیش هم اینه:
```bash
git checkout branch-name
git pull origin branch-name
```
واسه اد کردن و کامیت هم که با VS Code راحته .
و کدش میشه این:
```bash
git add .
git commit -m "commit message"
```
واسه پوش کردن هم که باز دکمه push تو VS Code و  کد دستیش:
```bash
git push origin branch_name
```
مرحله اخرم وقتی تغییرات تموم شد، میرین داخل GitHub و تو صفحه ریپو، روی Compare & Pull Request کلیک میکنیم.
بعد توضیح میدیم چه کاری کردیم.
و درخواست رو میزنیم به `dev` نه `main`.
حواسمون باشه به `main` نزنیم.

> [!IMPORTANT]
> هیچ‌کس مستقیم روی `main` یا `dev` کار نمی‌کنه! همه فقط روی شاخه‌های `feature/...` کار می‌کنن و با Pull Request تغییراتشون رو به `dev` می‌فرستن.

مرحله بعد هم مرج کردن به `main` هستش. که وقتی همه چیز تست شد اینکارو میکنیم:
```bash
git checkout main
git merge dev
git push origin main
```
### نکته‌های حرفه‌ای
- همیشه قبل از شروع کد:
```bash
git checkout dev
git pull origin dev
```
- قبل از Push کردن، مطمئن شو روی شاخه درست هستی:
```bash
git branch
```
- حتماً هر Commit Message باید معنی‌دار باشه:
```bash
git commit -m "Add login form validation"
```
