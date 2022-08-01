use coap_lite::{CoapRequest, RequestType as Method};
use color_eyre::eyre::Result;
use std::net::{SocketAddr, UdpSocket};

fn main() -> Result<()> {
    color_eyre::install()?;
    let mut request: CoapRequest<SocketAddr> = CoapRequest::new();
    request.set_method(Method::Post);
    request.set_path("/test");
    request.message.payload = b"Hello".to_vec();

    let socket = UdpSocket::bind("127.0.0.1:0")?;
    let packet = request.message.to_bytes()?;
    socket.send_to(&packet[..], "127.0.0.1:1331")?;
    Ok(())
}
