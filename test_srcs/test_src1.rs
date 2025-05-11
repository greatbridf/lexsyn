fn print(number: i32) {
    let _ = number;
}

fn main() {
    let a = 10 * 20 - 9;
    let mut b: i32 = 20;

    if a > 0 {
        print(b);
    } else {
        print(a);
    }

    while b == 0 {
        print(a);
    }

    return a;
}