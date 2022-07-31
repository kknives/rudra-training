use coap_lite::{CoapRequest, Packet, RequestType as Method};
use color_eyre::eyre::Result;
use console::Term;
use dialoguer::Input;
use eyre::eyre;
use pest::Parser;
use pest_derive::Parser;
use std::net::SocketAddr;
use std::thread;
use tokio::net::UdpSocket;
use tokio::runtime::Handle;
use tokio::sync::mpsc;

#[tokio::main]
async fn main() -> Result<()> {
    color_eyre::install()?;
    let mut prompt = Input::new();
    let (sender, receiver) = mpsc::channel(32);
    let handle = Handle::current();
    let net_thread = thread::spawn(move || {
        handle.spawn(listen_reply(receiver));
    });

    loop {
        let input: String = prompt.with_prompt("You").report(false).interact_text()?;
        if input == "quit" {
            sender.send(Command::Terminate).await?;
            break;
        } else {
            sender.send(Command::UserInput(input)).await?;
        }
    }

    net_thread
        .join()
        .map_err(|_| eyre!("Could not join network thread"))?;
    Ok(())
}

#[derive(Debug)]
enum Command {
    UserInput(String),
    Terminate,
}

async fn listen_reply(mut user: mpsc::Receiver<Command>) -> Result<()> {
    let socket = UdpSocket::bind("127.0.0.1:0").await?;
    let term = Term::stdout();
    term.write_line("Welcome to CoAP Chat Server!")?;
    loop {
        tokio::select! {
            request = handle_recv(&socket) => {
                let request = request?;
                let incoming = String::from_utf8(request.message.payload)?;
                term.write_line(&incoming)?;
            },
            producer = user.recv() => {
                let command = producer.ok_or_else(|| eyre!("Could not process input thread message"))?;
                match command {
                    Command::UserInput(content) => {
                        let mut recepient: Result<String, eyre::Error> = Err(eyre!("Could not parse message body"));
                        let mut body: Result<String, eyre::Error> = Err(eyre!("Could not parse message body"));

                        for token in Recepient::parse(Rule::message, &content)?.next()
                                            .ok_or_else(|| eyre!("Could not parse user input"))?.into_inner() {
                            match token.as_rule() {
                                Rule::id => {recepient = Ok(token.as_str().to_owned());},
                                Rule::body => {body = Ok(token.as_str().to_owned());},
                                _ => {},
                            };
                        }
                        handle_send(&socket, body?.into_bytes(), recepient?).await?;
                    },
                    Command::Terminate => { break; },
                };
            },
        }
    }
    Ok(())
}

#[derive(Parser)]
#[grammar = "message.pest"]
struct Recepient;

async fn handle_recv(socket: &UdpSocket) -> Result<CoapRequest<SocketAddr>> {
    let mut buf = [0; 1024];
    let (size, src) = socket.recv_from(&mut buf).await?;
    let packet = Packet::from_bytes(&buf[..size])?;
    Ok(CoapRequest::from_packet(packet, src))
}

async fn handle_send(socket: &UdpSocket, content: Vec<u8>, recepient: String) -> Result<()> {
    let mut request: CoapRequest<SocketAddr> = CoapRequest::new();
    request.set_method(Method::Post);
    request.set_path("/chat");
    request.message.payload = content;
    let raw_packet = request.message.to_bytes()?;
    socket.send_to(&raw_packet[..], recepient).await?;
    Ok(())
}
