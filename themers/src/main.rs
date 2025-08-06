use chrono::prelude::*;
use std::process::Command;

fn main() {

    // if is_light() {
    //     let is_light = true;
    // } else {
    //     let is_light = false;
    // }

    let (image_path, filename) = get_random_image_filename(is_light());


}

fn is_light() -> bool {
   // let now = SystemTime::now();
    let now = chrono::offset::Local::now();
    let hour = now.hour();

    if hour < 18 {
        true
    } else {
        false
    }
}

fn get_random_image_filename(is_light: bool) -> (String, String) {

    let path = if is_light {
        "~/Pictures/light"
    } else {
        "~/Pictures/dark"
    };

    let command = format!("ls {} | shuf -n 1", path);

    println!("{}", command);

    let output = Command::new("sh")
                         .arg("-c")
                         .arg(command)
                         .output()
                         .expect("failed to execute process");

    let raw_filename = output.stdout;
    let filename = String::from_utf8_lossy(&raw_filename);


    println!("{}", filename);

    let image_path = format!("{}/{}", &path, &filename);

    return (image_path.to_string(), filename.to_string());
}