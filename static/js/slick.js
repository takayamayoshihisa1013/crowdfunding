$(".slider").slick({
    // autoplay: true,       //自動再生
    // autoplaySpeed: 2000,  //自動再生のスピード
    // speed: 800,           //スライドするスピード
    // dots: true,           //スライド下のドット
    arrows: false,         //左右の矢印
    // infinite: true,       //永久にループさせる
    autoplay: true,         //自動再生
    autoplaySpeed: 1000,       //自動再生のスピード
    speed: 4000,            //追加（スライドスピード
    slidesToShow: 1,        //追加（スライドの1スライドごとの表示枚数
    // cssEase: "linear",      //追加（スライドの動きを等速に
    pauseOnHover: false,    //追加（ホバーしても止まらないように
    pauseOnFocus: false,    //追加（フォーカスしても止まらないように
})