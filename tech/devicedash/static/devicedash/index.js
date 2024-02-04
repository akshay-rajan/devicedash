function setDefaults(option, min, max) {
    document.getElementById('min').value = min;
    document.getElementById('max').value = max;
    
    document.forms[0].submit();
}

function validateForm() {
    var minPrice = parseInt(document.getElementById('min').value);
    var maxPrice = parseInt(document.getElementById('max').value);

    if (isNaN(minPrice) || isNaN(maxPrice)) {
        document.getElementById('validationMessage').innerText = 'Invalid Input!';
        return false;
    }

    if (minPrice > maxPrice) {
        document.getElementById('validationMessage').innerText = 'Minimum price cannot be greater than maximum price.';
        return false;
    }

    // Clear validation message if validation passes
    document.getElementById('validationMessage').innerText = '';
    return true;
}