
function toggleElement(){
    let className = document.getElementById("search-form-container").className.split(" ");
    if (className.includes("d-none")){
        className = className.filter(function(val, indx, arr){
            return val != "d-none"
        });
    }else{
        className.push("d-none")
    }
    document.getElementById("search-form-container").className = className.join(" ");
}

// function toggleElementForRoomManage(){
//     let className = document.getElementById("management-confirmation").className.split(" ");
//     if (className.includes("d-none")){
//         className = className.filter(function(val, indx, arr){
//             return val != "d-none"
//         });
//         document.getElementById("management-confirmation").focus({preventScroll:true})
//     }else{
//         className.push("d-none")
//     }
//     document.getElementById("management-confirmation").className = className.join(" ");
// }


