use coap_lite::{CoapRequest, Packet};
use color_eyre::eyre::Result;
use eyre::eyre;
use std::net::UdpSocket;

fn main() -> Result<()> {
    let socket = UdpSocket::bind("127.0.0.1:1331")?;
    color_eyre::install()?;
    let mut buf = [0; 100];
    let (size, src) = socket.recv_from(&mut buf)?;
    println!("Payload {:x?}", &buf[..size]);

    let packet = Packet::from_bytes(&buf[..size])?;
    let request = CoapRequest::from_packet(packet, src);

    let method = request.get_method().clone();
    let path = request.get_path();
    let payload = request.message.payload;

    println!(
        "Recieved CoAP request '{:?} {}' from {}. It said {}",
        method,
        path,
        src,
        String::from_utf8(payload)?
    );

    let mut response = request
        .response
        .ok_or_else(|| eyre!("Could not create response"))?;
    response.message.payload = b"OK".to_vec();

    let packet = response.message.to_bytes()?;
    socket.send_to(&packet[..], &src)?;
    Ok(())
}
