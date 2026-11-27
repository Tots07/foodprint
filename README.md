# FoodPrint

Suivi des repas, bilan carbone, eau et alcool. Une seule page (`index.html`), sans build.

## Déploiement sur GitHub Pages
1. Créez un dépôt GitHub et déposez le contenu de ce dossier à la racine (`index.html` doit être à la racine).
2. Settings > Pages > Source : "Deploy from a branch", branche `main`, dossier `/ (root)`.
3. L'application sera disponible sur `https://<utilisateur>.github.io/<depot>/`.

## Firebase (Firestore)
L'application lit/écrit la collection `sessions` dans Firestore (projet `alimentation-2fa9c`).
Sans règles adaptées, les écritures échouent et l'app retombe sur le stockage local du navigateur.
Dans la console Firebase > Firestore > Règles, autorisez par exemple :

    rules_version = '2';
    service cloud.firestore {
      match /databases/{database}/documents {
        match /sessions/{id} { allow read, write: if true; }
      }
    }

Attention : le code PIN est haché (SHA-256) côté navigateur, mais avec ces règles n'importe qui connaissant
la configuration peut lire la base. Pour une vraie sécurité, utilisez Firebase Auth.

## Installation sur mobile (PWA)
L'application a son propre `manifest.json` (id `foodprint-app`, scope `./`) et un `sw.js`, ce qui la distingue des autres applications hébergées sur le même domaine `github.io`.

## Sessions et code PIN
Un visiteur qui choisit une session la voit en lecture seule. Pour modifier, il saisit le code PIN (bouton Déverrouiller). Cette protection est côté application : tant que les règles Firestore sont ouvertes, elle ne bloque pas un accès direct à la base.

## Application Android (APK) via GitHub Actions
Le workflow `.github/workflows/android.yml` emballe l'application avec Capacitor, signe l'APK et l'envoie aux testeurs via Firebase App Distribution.
Secrets à créer dans GitHub (Settings > Secrets and variables > Actions) :
ANDROID_KEYSTORE_B64, ANDROID_KEYSTORE_PASSWORD, ANDROID_KEY_ALIAS, ANDROID_KEY_PASSWORD, FIREBASE_ANDROID_APP_ID, FIREBASE_SERVICE_ACCOUNT, FIREBASE_TESTERS.
L'identifiant de l'application (`com.foodprint.app`) est dans `capacitor.config.json` : à choisir avant la première distribution.
