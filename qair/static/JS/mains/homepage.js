window.onload = function () {
    main()
}

var pillsBook = document.getElementById("pills-book")
var pillsmytrip = document.getElementById("pills-mytrip")
var pillscheckin = document.getElementById("pills-checkin")
var pillsflightstatus = document.getElementById("pills-flightstatus")

function onPillClick(str){
    if(str === 'book'){
        pillsBook.className = 'd-block'
        pillsmytrip.className = 'd-none'
        pillscheckin.className = 'd-none'
        pillsflightstatus.className = 'd-none'
    }
    else if(str === 'mytrip'){
        pillsBook.className = 'd-none'
        pillsmytrip.className = 'd-block'
        pillscheckin.className = 'd-none'
        pillsflightstatus.className = 'd-none'
    }
    else if(str === 'checkin'){
        pillsBook.className = 'd-none'
        pillsmytrip.className = 'd-none'
        pillscheckin.className = 'd-block'
        pillsflightstatus.className = 'd-none'
    }
    else if(str === 'flightstatus'){
        pillsBook.className = 'd-none'
        pillsmytrip.className = 'd-none'
        pillscheckin.className = 'd-none'
        pillsflightstatus.className = 'd-block'
    }

}