const lanIP = `${window.location.hostname}:5000`;
const socket = io(`http://${lanIP}/`);

let htmlSubmitbtn;
let htmlFeedbtn;
let htmlHistory;

let autofeedsetting = 0;
let counterTFT;
let time;

try {
  counterTFT = JSON.parse(localStorage.getItem('x'))['counterTFT'];
  time = JSON.parse(localStorage.getItem('x'))['time'];
} catch (error) {
  console.log("error counterTFT / time");
};

let today = new Date();
todayHours = today.getHours();
todayMinutes = today.getMinutes();
let yesterday;

//HoursMinutes = String(todayHours) + ':' + String(todayMinutes);

//const clearClassList = function (el) {
//  el.classList.remove("c-donker");
//  el.classList.remove("c-licht");
//};

if (todayHours == 23 && todayMinutes == 59) {
  yesterday = today;
  console.log('new day')
}

if (today == yesterday) {
  t = JSON.parse(localStorage.getItem('x'))['time'];
  localStorage.setItem('x', JSON.stringify({
    counterTFT: 0,
    time: t
  }))
  console.log('reset!')
}

const listenToUI = function () {
  if (htmlHistory) {
    socket.emit("F2B_history");
  }

  if (htmlSubmitbtn) {
    btn = document.querySelector('.js-submit');
    btn.addEventListener('click', function () {
      globalThis.timeofday = document.querySelector('.js-timeofday').value;
      globalThis.everyday = document.querySelector('.js-everyday').value;
      if (everyday != null && timeofday != null) {
        console.log(timeofday);
        console.log(everyday);
        //if (everyday == 1){
        //  socket.emit("F2B_autofeedeveryday", {'timeofday': timeofday});
        //}
        //if (everyday == 0){
        //  socket.emit("F2B_autofeedonce", {'timeofday': timeofday});
        //}

        socket.emit("F2B_autofeed", {'timeofday': timeofday, 'everyday': everyday});
      };
    });
  };

  if (htmlFeedBtn){
    var d = new Date().toJSON().slice(0,10);
    var d2 = new Date()
    year = d.slice(0, 4);
    month = d.slice(5, 7);
    day = d.slice(8, 10);
    hours = d2.getHours()
    minutes = d2.getMinutes()

    if (minutes < 10){
      fullDate = String(hours) + ':0' + String(minutes) + '<br >' + String(day) + ' ' + String(month) + ' ' + String(year);
      document.getElementById("js-date").innerHTML = fullDate;
    }

    if (minutes >= 10) {
      fullDate = String(hours) + ':' + String(minutes) + '<br >' + String(day) + ' ' + String(month) + ' ' + String(year);
      document.getElementById("js-date").innerHTML = fullDate;
    }

    document.getElementById("js-feedtime").innerHTML = time;
    document.getElementById("js-feedtimetoday").innerHTML = counterTFT;
    document.getElementById("js-btn").addEventListener("click", function () {
      console.log('click!');
      counterTFT++;

      var date = new Date();
      if (date.getMinutes() < 10){
        t = date.getHours() + ":0" + date.getMinutes()
      }

      if (date.getMinutes() >= 10){
        t = date.getHours() + ":" + date.getMinutes()
      }

      localStorage.setItem('x', JSON.stringify({
        counterTFT: counterTFT,
        time: t
      }));

      document.getElementById("js-feedtime").innerHTML = JSON.parse(localStorage.getItem('x'))['time'];
      document.getElementById("js-feedtimetoday").innerHTML = JSON.parse(localStorage.getItem('x'))['counterTFT'];
      //document.getElementById("js-feedtime").innerHTML = localStorage.getItem("time");
      //document.getElementById("js-feedtimetoday").innerHTML = localStorage.getItem("counterTFT");
      socket.emit("F2B_change_Motor_Value");
    });

    document.getElementById("js-autobtn").addEventListener("click", function () {
      autofeedsetting++;
      console.log('click!');
      if (autofeedsetting >= 2){
        autofeedsetting = 0;
      }

      if (autofeedsetting == 1){
        document.getElementById("js-autobtn").innerHTML = `<button class=" o-layout__button o-layout__buttongreen u-color-primary-base">
        ON
      </button>`
      }

      if (autofeedsetting == 0){
        document.getElementById("js-autobtn").innerHTML = `<button class=" o-layout__button o-layout__buttonred u-color-primary-base">
        OFF
      </button>`
      }
    });
  };
};

const listenToSocket = function () {
  socket.on("connected", function () {
    console.log("verbonden met socket webserver");
  });

  socket.on("B2F_history", function (jsonString) {
    console.log('history');
    //console.log(jsonString);
    jsonObject = JSON.parse(jsonString);
    //console.log(jsonObject)

    historyInnerHTML = '';
    let actie = '';
    let datum;
    let waarde;

    for(i=0; i < jsonObject.length; i++) {
      //console.log(jsonObject[i]);

      if (jsonObject[i].ActieID == 1) {
        actie = 'lichtintensiteit inlezen';
      }

      if (jsonObject[i].ActieID == 2) {
        actie = 'beweging detecteren';
      }

      if (jsonObject[i].ActieID == 3) {
        actie = 'motor draaien';
      }

      if (jsonObject[i].ActieID == 4) {
        actie = 'gewicht inlezen';
      }

      if (jsonObject[i].ActieID == 5) {
        actie = 'leds aan';
      }

      if (jsonObject[i].ActieID == 6) {
        actie = 'leds uit';
      }

      if (jsonObject[i].ActieID == 7) {
        actie = 'eten geven';
      }

      datum = jsonObject[i].Datum;

      waarde = jsonObject[i].Waarde;

      //row = JSON.stringify(jsonObject[i]);
      //console.log(row);

      historyInnerHTML += `<p>${datum} | ${actie} | ${waarde}</p>`
    };

    document.getElementById("js-showHistory").innerHTML = historyInnerHTML
  });

  //socket.on("B2F_status", function (jsonObject) {
  //  console.log("Dit is de status");
  //  console.log(jsonObject);
    //document.getElementById("date").innerHTML = jsonObject.date
  //});

  socket.on("B2F_date", function (jsonObject) {
    console.log("Dit is de datum");
    console.log(jsonObject);
  });

  socket.on("B2F_verandering_LDR", function (jsonObject) {
    console.log("status van LDR is veranderd");
    //console.log(jsonObject);
    x = 0;
    x = jsonObject.LDR;
    console.log(x);
    //image = document.querySelector(`.js-licht`)
    //clearClassList(image)
    if (x <= 500) {
      //mijnInnerHTML += `<img src="/style/img/zon.png" alt="Licht">`
      //image.classList.add("c-licht");
    }

    if (x > 500) {
      //mijnInnerHTML += `<img src="/style/img/maan.png" alt="Donker">`
      //image.classList.add("c-donker");
    }
  })

  socket.on("B2F_verandering_Motor", function (jsonObject) {
    console.log("status van Motor is veranderd");
    console.log(jsonObject.Motor.waarde)
  })

  socket.on("B2F_verandering_PIR", function (jsonObject) {
    console.log("status van PIR is veranderd");
    console.log(jsonObject.PIR.waarde)
  })

  socket.on("B2F_verandering_HX711", function (jsonObject) {
    console.log("status van HX711 is veranderd");
    console.log(jsonObject.HX711)

    if (htmlFeedBtn) {
      // leeg
      if (jsonObject.HX711 > 1166.99) {
        document.getElementById("js-foodmeter").innerHTML = `<div class="u-fixed-width-sm u-fixed-width-xs o-layout__meter o-layout__layer1">
      </div>`
      };

      // 10% vol
      if (jsonObject.HX711 < 1165.99) {
        document.getElementById("js-foodmeter").innerHTML = `<div class="u-fixed-width-sm u-fixed-width-xs o-layout__meter o-layout__layer1">
      </div>
      <div class="o-layout__meter o-layout__layer2 o-layout__layer10">
      </div>`
      };

      // 20% vol
      if (jsonObject.HX711 < 1164) {
        document.getElementById("js-foodmeter").innerHTML = `<div class="u-fixed-width-sm u-fixed-width-xs o-layout__meter o-layout__layer1">
      </div>
      <div class="o-layout__meter o-layout__layer2 o-layout__layer20">
      </div>`
      };

      // 30% vol
      if (jsonObject.HX711 < 1163) {
        document.getElementById("js-foodmeter").innerHTML = `<div class="u-fixed-width-sm u-fixed-width-xs o-layout__meter o-layout__layer1">
      </div>
      <div class="o-layout__meter o-layout__layer2 o-layout__layer30">
      </div>`
      };

      // 40% vol
      if (jsonObject.HX711 < 1162) {
        document.getElementById("js-foodmeter").innerHTML = `<div class="u-fixed-width-sm u-fixed-width-xs o-layout__meter o-layout__layer1">
      </div>
      <div class="o-layout__meter o-layout__layer2 o-layout__layer40">
      </div>`
      };

      // 50% vol
      if (jsonObject.HX711 < 1162) {
        document.getElementById("js-foodmeter").innerHTML = `<div class="u-fixed-width-sm u-fixed-width-xs o-layout__meter o-layout__layer1">
      </div>
      <div class="o-layout__meter o-layout__layer2 o-layout__layer50">
      </div>`
      };

      // 60% vol
      if (jsonObject.HX711 < 1161) {
        document.getElementById("js-foodmeter").innerHTML = `<div class="u-fixed-width-sm u-fixed-width-xs o-layout__meter o-layout__layer1">
      </div>
      <div class="o-layout__meter o-layout__layer2 o-layout__layer60">
      </div>`
      };

      // 70% vol
      if (jsonObject.HX711 < 1160) {
        document.getElementById("js-foodmeter").innerHTML = `<div class="u-fixed-width-sm u-fixed-width-xs o-layout__meter o-layout__layer1">
      </div>
      <div class="o-layout__meter o-layout__layer2 o-layout__layer70">
      </div>`
      };

      // 80% vol
      if (jsonObject.HX711 < 1159) {
        document.getElementById("js-foodmeter").innerHTML = `<div class="u-fixed-width-sm u-fixed-width-xs o-layout__meter o-layout__layer1">
      </div>
      <div class="o-layout__meter o-layout__layer2 o-layout__layer80">
      </div>`
      };

      // 90% vol
      if (jsonObject.HX711 < 1158) {
        document.getElementById("js-foodmeter").innerHTML = `<div class="u-fixed-width-sm u-fixed-width-xs o-layout__meter o-layout__layer1">
      </div>
      <div class="o-layout__meter o-layout__layer2 o-layout__layer90">
      </div>`
      };

      // 100% vol
      if (jsonObject.HX711 < 1157) {
        document.getElementById("js-foodmeter").innerHTML = `<div class="u-fixed-width-sm u-fixed-width-xs o-layout__meter o-layout__layer1">
      </div>
      <div class="o-layout__meter o-layout__layer2 o-layout__layer100">
      </div>`
      };
    }
  });
};

document.addEventListener("DOMContentLoaded", function () {
  console.info("DOM geladen");
  htmlSubmitbtn = document.querySelector('.js-submitbtn');
  htmlFeedBtn = document.querySelector('.js-feedbtn');
  htmlHistory = document.querySelector('.js-history');
  listenToUI();
  listenToSocket();
});
