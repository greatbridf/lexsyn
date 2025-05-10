fn print(number: i32) {
    let _ = number;
}

fn main() {
    let a: i32=10;
    let mut b: i32 = 20;

    loop {
        b= b   -1;
        if b==0 {
            break;
        }
    }

    while 0 == 0 {
        ;
    }

    for item in range(0, 10) {
        if item > 7 {
            continue;
        } else {
            print(item / 3);
        }
    }

    return a;
}
