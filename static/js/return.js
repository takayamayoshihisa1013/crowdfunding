document.addEventListener("DOMContentLoaded", function() {

    document.getElementById("check").addEventListener("click", function() {
        const checkboxes = document.querySelectorAll('input[type="checkbox"][name="return_select"]');

        checkboxes.forEach(function(checkbox) {
            if (!checkbox.checked) {
                checkbox.closest("label").style.display = "none";
            }

            checkbox.disabled = true;
        })

        document.getElementById("return").style.display = "block";
        document.getElementById("support").style.display = "block";
        document.getElementById("check").style.display = "none";

    })

    document.getElementById("return").addEventListener("click", function() {
        const checkboxes = document.querySelectorAll('input[type="checkbox"][name="return_select"]');

        checkboxes.forEach(function(checkbox) {
            checkbox.closest("label").style.display = "block";

            checkbox.disabled = false;
        })

        document.getElementById("return").style.display = "none";
        document.getElementById("support").style.display = "none";
        document.getElementById("check").style.display = "block";
    })

})