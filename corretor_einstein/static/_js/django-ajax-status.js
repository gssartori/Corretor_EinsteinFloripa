setInterval(function() {
    $.ajax(
    {
        type: "GET",
        url: "status_relatorios_ajax",  // URL to your view that serves new info
        success : function(response){
            $.each(response['novos_status'], function(){
                $.each(this, function(nome_aluno, status_aluno){
                    $("#"+nome_aluno).html(status_aluno);
                });
            });
        },
        error : function(xhr) { console.log('Erro') }
    })}, 10000)
////    .done(function(response) {
////        $('#_appendHere').append(response);
////        append_increment += 10;

//var t = function() {
//    $.ajax(
//    {
//        type: "GET",
//        url: "status_relatorios_ajax",  // URL to your view that serves new info
//        success : function(response){
//            console.log()
//            $.each(response['novos_status'], function(){
//                $.each(this, function(nome_aluno, status_aluno){
//                    $("#"+nome_aluno).html(status_aluno)
//                });
//            });
//        },
//        error : function(xhr) { console.log('Erro') }
//    })}
//t()
