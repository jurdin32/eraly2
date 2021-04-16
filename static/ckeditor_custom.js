function ckeditor_(control){
    CKEDITOR.replace(control,{
    toolbar : [
        ['TextColor', 'BGColor','-','Image', 'Table','-'],
        ['Bold', 'Italic', 'Underline', 'Strike', 'Subscript', 'Superscript'],
        ['-','NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-', 'Blockquote', 'CreateDiv', '-',
               'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock']
    ]
});
}