setInterval(function() {
    $.ajax(
    {
        type: "GET",
        url: "atualiza_pagina_ajax",  // URL to your view that serves new info
        success : function(response){
            $.each(response['novos_status'], function(){
                $.each(this, function(nome_aluno, status_aluno){
                    $("#"+nome_aluno).html(status_aluno);
                });
            });
        },
        error : function(xhr) { console.log('Erro') }
    })}, 5000)
