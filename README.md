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
