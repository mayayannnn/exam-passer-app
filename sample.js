function change() {
	const submitBtn = document.getElementById('button');
	const checkboxes = document.querySelectorAll('input[name="main_category"]:checked');
	if (checkboxes.length === 0) {
		submitBtn.disabled = true;
	} else {
		submitBtn.disabled = false;
	}
}