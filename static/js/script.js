document.addEventListener('DOMContentLoaded', () => {
    const cartTrigger = document.getElementById('cart-trigger');
    const closeCart = document.getElementById('close-cart');
    const drawer = document.getElementById('cart-drawer');

    // Open Cart
    cartTrigger.addEventListener('click', () => {
        drawer.classList.remove('translate-x-full');
    });

    // Close Cart
    closeCart.addEventListener('click', () => {
        drawer.classList.add('translate-x-full');
    });
});
document.getElementById('location-trigger').addEventListener('click', () => {
    const locationText = document.getElementById('location-text');
    
    if (navigator.geolocation) {
        locationText.innerText = "Detecting...";
        
        navigator.geolocation.getCurrentPosition(async (position) => {
            const { latitude, longitude } = position.coords;
            
            try {
                // Fetching address from coordinates using OpenStreetMap API
                const response = await fetch(`https://nominatim.openstreetmap.org/reverse?format=json&lat=${latitude}&lon=${longitude}`);
                const data = await response.json();
                
                // Extracting City and State/Country
                const city = data.address.city || data.address.town || data.address.village;
                const state = data.address.state;
                
                locationText.innerText = `${city}, ${state}`;
            } catch (error) {
                locationText.innerText = "Error fetching location";
            }
        }, (err) => {
            locationText.innerText = "Access Denied";
        });
    } else {
        alert("Geolocation is not supported by your browser.");
    }
});
// When the register button is clicked:
localStorage.setItem('userAddress', document.getElementById('address').value);
// Google Login Action
document.getElementById('google-login-btn').addEventListener('click', () => {
    console.log("Google button clicked! Redirecting to Google Auth...");
    // Firebase example:
    // const provider = new firebase.auth.GoogleAuthProvider();
    // firebase.auth().signInWithPopup(provider);
});

// Apple Login Action
document.getElementById('apple-login-btn').addEventListener('click', () => {
    alert("Apple login is coming soon!");
});