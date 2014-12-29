$(window).on('load', function () {

  $('#id_groups').multiSelect();

  $('#id_full_name').html($('#id_first_name').val() + ' ' + $('#id_last_name').val());
  $('#id_first_name, #id_last_name').on('keyup', function() {
    $('#id_full_name').html($('#id_first_name').val() + ' ' + $('#id_last_name').val());
  });

  if ($('#id_auto_uid').prop('checked')) {
    $('#id_auto_uid').parent().addClass('active');
    $('#id_uid').prop('disabled', true);
  }
  if ($('#id_auto_home').prop('checked')) {
    $('#id_auto_home').parent().addClass('active');
    $('#id_home_directory').prop('disabled', true);
  }
  if ($('#id_auto_email').prop('checked')) {
    $('#id_auto_email').parent().addClass('active');
    $('#id_email').prop('disabled', true);
  }

  $('#id_auto_uid').change( function() {
    $('#id_uid').prop('disabled', $(this).prop('checked'));
  });
  $('#id_auto_home').change( function() {
    $('#id_home_directory').prop('disabled', $(this).prop('checked'));
  });
  $('#id_auto_email').change( function() {
    $('#id_email').prop('disabled', $(this).prop('checked'));
  });

});
