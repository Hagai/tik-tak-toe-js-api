
var game_status = "Started"
var player_sign = "X"

function switch_player(){
    if (player_sign == "X"){
       player_sign = "O"
    }
    else if (player_sign == "O"){
           player_sign = "X"
    }
    else {
        alert("Unknonw player sign :" + player_sign)
    }
    $("#p_player_id").text("Turn player: " + player_sign)
}

function is_all_cell_chosen(){
    var all_cell_chosen = true
    var cell_list = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    for (cell_i in cell_list){
        if ( ($("#cell_"+(cell_list[cell_i])).text() == "X") || ($("#cell_"+(cell_list[cell_i])).text() == "O")){
             
        }
        else {
            all_cell_chosen = false
        }
    }
    return all_cell_chosen
}

function is_3_in_row(row_i, player_sign){
    var is_win = false    
    if (($("#cell_"+((row_i-1)*3+1)).text() == player_sign) && ($("#cell_"+((row_i-1)*3+2)).text() == player_sign) && ($("#cell_"+((row_i-1)*3+3)).text() == player_sign)) {
        is_win = true
    }
    return is_win
}

function is_3_in_column(column_i, player_sign){
    var is_win = false
    // console.log("is_3_in_column(" + column_i +", " + player_sign + ")")
    if (($("#cell_"+(column_i)).text() == player_sign) && ($("#cell_"+(3 + column_i)).text() == player_sign) && ($("#cell_"+(6 +column_i)).text() == player_sign)) {
        is_win = true
    }
    return is_win
}

function is_3_in_primary_diagonal(player_sign){
    var is_win = false
    if (($("#cell_1").text() == player_sign) && ($("#cell_5").text() == player_sign) && ($("#cell_9").text() == player_sign)) {
        is_win = true
    }
    return is_win
}

function is_3_in_secondary_diagonal(player_sign){
    var is_win = false
    if (($("#cell_7").text() == player_sign) && ($("#cell_5").text() == player_sign) && ($("#cell_3").text() == player_sign)) {
        is_win = true
    }
    return is_win
}

function is_player_won(player_sign){
    var is_win = false
    var row_i
    var row_list = [1, 2, 3]
    for (row_i in row_list){
        if (is_3_in_row(row_list[row_i], player_sign)){
            is_win = true
             
        }
    }
    var column_i
    var column_list = [1, 2, 3]
    for (column_i in column_list){
        if (is_3_in_column(column_list[column_i], player_sign)){
            is_win = true
            
        }
    }
    if (is_3_in_primary_diagonal(player_sign) || is_3_in_secondary_diagonal(player_sign)){
        is_win = true
    }
    return is_win
}

function update_game_status(){
    var new_text = ""
    if (is_player_won(player_sign)){
        new_text = "Player: " + player_sign + " has won!"
        $("#p_game_status").text(new_text)
        game_status = "Ended"
    }
    else if (is_all_cell_chosen()){
        new_text = "Nobody wins"
        $("#p_game_status").text(new_text)
        game_status = "Ended"
    
    }
    else{

    }
}

$(document).ready(function(){
	$(".tik_tak_toe_cell").click(function(){
        if (game_status=="Ended"){
            return
        }
        if ( ($(this).text() == "X") || ($(this).text() == "O") ){
                alert("This cell was choosed already!")
                return
            }
//        fill the cell text with the player mark
        $(this).text(player_sign);

        update_game_status()
        if (game_status == "Ended"){
            return
        }
        else{
            switch_player()
        }
        
	});
});
