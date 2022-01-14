$('form').submit(function() {
    $(':input', this).each(function() {
        this.disabled = !($(this).val());
    });
});

$('.formreset').click(resetForm);
function resetForm() {
    const $form = $('#filterForm')
    $form.find('input:text, input:password, input:file, select, textarea').val('');
    $form.find(':input[type=number]').val('');
    $form.find('input:radio, input:checkbox')
         .removeAttr('checked').removeAttr('selected');
}

document.querySelector("#darkmode").onclick = function(){
    darkmode.toggleDarkMode();
}

const elements = document.querySelectorAll('.clip')
for (let i = 0, element; element = elements[i]; i++) {
    element.addEventListener('click', function() {
        navigator.clipboard.writeText(element.dataset.value);
    });
}