
// Shadow std::option::Option deliberately for quickly testing
// find references in Sourcegraph UI.
#[derive(PartialEq, Eq)]
enum Option<A> {
    Some(A),
    None
}

fn main() {
    use crate::Option::*;
    let _ = Some(std::option::Option::Some(0)) == None;
    println!("Hello, world!");
}
