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
            $.each(response['alertas'], function(){
                $.each(this, function(titulo, mensagem){
                    console.log(response['alertas'])
                    $("#titulo-alerta").html(titulo);
                    $("#mensagem-alerta").html(mensagem);
                    $("acionador").trigger( "click" );
                });
            });
        },
        error : function(xhr) { console.log('Erro') }
    })}, 9800)