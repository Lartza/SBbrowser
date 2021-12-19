if (localStorage.getItem('theme') !== null && localStorage.getItem('theme') === 'light') {
    $('body').toggleClass('bootstrap bootstrap-dark');
}

$('#css_toggle').click(function() {
  $('body').toggleClass('bootstrap bootstrap-dark');
  if (localStorage.getItem('theme') === null || localStorage.getItem('theme') === 'dark') {
      localStorage.setItem('theme', 'light');
  } else {
      localStorage.setItem('theme', 'dark');
  }
});

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