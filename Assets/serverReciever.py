import socket
import argparse
import os

# Tentukan folder default = lokasi file ini berada
DEFAULT_SAVE_DIR = os.path.dirname(os.path.abspath(__file__))


def recv_until_newline(conn):
    """Menerima nama file sampai newline (\n) tanpa terkena binary file."""
    buffer = b""
    while True:
        byte = conn.recv(1)
        if not byte:
            break
        if byte == b"\n":
            break
        buffer += byte
    return buffer.decode("utf-8")


def main():
    parser = argparse.ArgumentParser(
        description="Simple File Receiver Server"
    )

    parser.add_argument(
        "--host", "-H",
        type=str,
        default="localhost",
        help="Host untuk server (default: localhost)"
    )

    parser.add_argument(
        "--port", "-P",
        type=int,
        default=5000,
        help="Port untuk server (default: 5000)"
    )

    args = parser.parse_args()

    HOST = args.host
    PORT = args.port

    print("=== File Receiver Server ===")
    print(f"Host        : {HOST}")
    print(f"Port        : {PORT}")
    print(f"Save Folder : {DEFAULT_SAVE_DIR}")
    print("\nMenunggu client...\n")

    # Setup socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen(1)

    conn, addr = s.accept()
    print(f"[CONNECTED] Client: {addr}")

    # =====================================
    # Terima nama file dengan aman
    # =====================================
    filename = recv_until_newline(conn).strip()
    filepath = os.path.join(DEFAULT_SAVE_DIR, filename)

    print(f"[INFO] Nama file diterima: {filename}")
    print(f"[INFO] Menyimpan ke: {filepath}")

    # =====================================
    # Terima isi file (binary)
    # =====================================
    with open(filepath, "wb") as f:
        while True:
            data = conn.recv(4096)
            if not data:
                break
            f.write(data)

    print(f"\n[SUCCESS] File diterima dan disimpan sebagai: {filepath}")

    conn.close()
    s.close()
    print("[SERVER CLOSED] Server dimatikan.")


if __name__ == "__main__":
    main()
