$('form').submit(function() {
    $(':input', this).each(function() {
        this.disabled = !($(this).val());
    });
});

function resetForm($form) {
    $form.find('input:text, input:password, input:file, select, textarea').val('');
    $form.find(':input[type=number]').val('');
    $form.find('input:radio, input:checkbox')
         .removeAttr('checked').removeAttr('selected');
}