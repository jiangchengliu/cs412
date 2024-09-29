document.addEventListener('DOMContentLoaded', function () {
    const spicyMisoCheckbox = document.getElementById('spicy-miso-checkbox');
    const extraMeatDiv = document.getElementById('extra-meat');

    
    if (spicyMisoCheckbox && extraMeatDiv) {
        spicyMisoCheckbox.addEventListener('change', function() {
            if (this.checked) {
                extraMeatDiv.style.display = 'block'; 
                console.log("success");
            } else {
                extraMeatDiv.style.display = 'none';
            }
        });
    } else {
        console.error("spicyMisoCheckbox or extraMeatDiv not found in the DOM");
    }
});
