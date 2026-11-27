import re, sys, pathlib
n = sys.argv[1]
mf = pathlib.Path('android/app/src/main/AndroidManifest.xml')
t = mf.read_text()
for p in ['POST_NOTIFICATIONS', 'SCHEDULE_EXACT_ALARM', 'RECEIVE_BOOT_COMPLETED']:
    if 'android.permission.' + p not in t:
        t = t.replace('<application', '<uses-permission android:name="android.permission.%s" />\n    <application' % p, 1)
mf.write_text(t)
for g in ('build.gradle', 'build.gradle.kts'):
    f = pathlib.Path('android/app') / g
    if f.exists():
        s = f.read_text()
        s = re.sub(r'(versionCode[ =]+)\d+', lambda m: m.group(1) + n, s, count=1)
        s = re.sub(r'(versionName[ =]+)"[^"]*"', lambda m: m.group(1) + '"1.0.' + n + '"', s, count=1)
        f.write_text(s)
print('android patched, build', n)
