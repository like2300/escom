
// Récupère le bouton par son ID
const loginButton = document.getElementById('login');

// Crée la fonction pour afficher le formulaire
function showLoginForm() {
    // Crée un overlay (fond semi-transparent)
    const overlay = document.createElement('div');
    overlay.style.position = 'fixed';
    overlay.style.top = '0';
    overlay.style.left = '0';
    overlay.style.width = '100%';
    overlay.style.height = '100%';
    overlay.style.backgroundColor = 'rgba(0, 0, 0, 0.5)';
    overlay.style.display = 'flex';
    overlay.style.justifyContent = 'center';
    overlay.style.alignItems = 'center';
    overlay.style.zIndex = '1000';
    
    // Crée le formulaire
    const loginForm = document.createElement('div');
    loginForm.style.backgroundColor = 'white';
    loginForm.style.padding = '20px';
    loginForm.style.borderRadius = '8px';
    loginForm.style.width = '300px';
    
    // Contenu du formulaire
    loginForm.innerHTML = `
        <h2 style="text-align: center; margin-bottom: 20px;">Connexion</h2>
        <form id="loginForm">
            <div style="margin-bottom: 15px;">
                <label for="username" style="display: block; margin-bottom: 5px;">Nom d'utilisateur</label>
                <input type="text" id="username" name="username" style="width: 100%; padding: 8px; box-sizing: border-box;">
            </div>
            <div style="margin-bottom: 15px;">
                <label for="password" style="display: block; margin-bottom: 5px;">Mot de passe</label>
                <input type="password" id="password" name="password" style="width: 100%; padding: 8px; box-sizing: border-box;">
            </div>
            <button type="submit" style="width: 100%; padding: 10px; background-color: #4CAF50; color: white; border: none; border-radius: 4px; cursor: pointer;">Se connecter</button>
        </form>
        <button id="closeForm" style="width: 100%; padding: 10px; margin-top: 10px; background-color: #f44336; color: white; border: none; border-radius: 4px; cursor: pointer;">Fermer</button>
    `;
    
    // Ajoute le formulaire à l'overlay
    overlay.appendChild(loginForm);
    
    // Ajoute l'overlay au body
    document.body.appendChild(overlay);
    
    // Ferme le formulaire quand on clique sur le bouton Fermer
    const closeButton = loginForm.querySelector('#closeForm');
    closeButton.addEventListener('click', function() {
        document.body.removeChild(overlay);
    });
    
    // Empêche la propagation du clic sur le formulaire
    loginForm.addEventListener('click', function(e) {
        e.stopPropagation();
    });
    
    // Ferme le formulaire quand on clique en dehors
    overlay.addEventListener('click', function() {
        document.body.removeChild(overlay);
    });
    
    // Gère la soumission du formulaire
    const form = loginForm.querySelector('#loginForm');
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        // Ici vous pouvez ajouter la logique de connexion
        alert('Formulaire soumis!');
    });
}

// Ajoute l'événement click au bouton
loginButton.addEventListener('click', showLoginForm);
