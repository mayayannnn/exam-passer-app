function change() {
    const submitBtn = document.getElementById('button');
    const mainCategoryCheckboxes = document.querySelectorAll('input[name="main_category"]:checked');
    const yearCheckboxes = document.querySelectorAll('input[name="year"]:checked');
    
    if (mainCategoryCheckboxes.length > 0 || yearCheckboxes.length > 0) {
        submitBtn.disabled = false;
    } else {
        submitBtn.disabled = true;
    }
}