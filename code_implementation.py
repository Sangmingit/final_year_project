import pyshark
import matplotlib.pyplot as plt

def load_capture_file():
    # Prompt the user for the path to the capture file
    file_path = input("Enter the full path to the Wireshark capture file: ")
    # Load the packet capture file using pyshark
    cap = pyshark.FileCapture(file_path)
    return cap

def identify_coexistence_method(cap):
    ipv4_count = 0
    ipv6_count = 0
    has_aaaa_record = False  # Flag to check for AAAA records

    for packet in cap:
        if 'IP' in packet:
            ipv4_count += 1
        elif 'IPv6' in packet:
            ipv6_count += 1
        elif 'DNS' in packet and 'AAAA' in packet:  # Check for AAAA DNS records
            has_aaaa_record = True

    if ipv4_count > 0 and ipv6_count > 0:
        if has_aaaa_record:
            return "Dual Stack"  # If AAAA records are found, it suggests Dual Stack

        # Continue with other dual-stack checks
        for packet in cap:
            if 'IPv6' in packet:
                if '::ffff:' in packet.ipv6.src or '::ffff:' in packet.ipv6.dst:
                    return "Dual Stack"
                elif packet.ipv6.src.startswith('fe80:') or packet.ipv6.dst.startswith('fe80:'):
                    return "Dual Stack"
                elif '2002:' in packet.ipv6.src or '2002:' in packet.ipv6.dst:
                    return "6to4 Tunneling"
                elif '64:ff9b::' in packet.ipv6.src or '64:ff9b::' in packet.ipv6.dst:
                    return "IPv6 over IPv4 Tunneling (e.g., 6in4)"
                elif '2001:' in packet.ipv6.src or '2001:' in packet.ipv6.dst:
                    return "Teredo Tunneling"

        return "IPv6 Only"
    elif ipv4_count > 0:
        return "IPv4 Only"
    elif ipv6_count > 0:
        return "IPv6 Only"
    else:
        return "Unknown Coexistence Method"

def analyze_ipv6_usage(cap):
    total_frames = 0
    ipv6_count = 0
    for packet in cap:
        total_frames += 1
        if 'IPv6' in packet:
            ipv6_count += 1

    # Calculate the IPv6 usage ratio and print it
    ipv6_ratio = ipv6_count / total_frames if total_frames > 0 else 0
    print(f"Total frames: {total_frames}")
    print(f"Total IPv6 packets: {ipv6_count}")
    print(f"IPv6 Usage Ratio: {ipv6_ratio:.2%}")  # Display the IPv6 ratio in the command line

    # Visualization 
    fig, ax = plt.subplots()
    bars = ax.bar(['Total Frames', 'IPv6 Packets'], [total_frames, ipv6_count], color=['blue', 'green'])

    # Display the counts above the bars
    for bar in bars:
        yval = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, yval, f'{int(yval)}', va='bottom', ha='center')

    ax.set_ylabel('Counts')
    ax.set_title('IPv6 Usage Analysis')
    plt.show()

def calculate_metrics(cap, src_ip, dst_ip, analyze_ipv4=True, analyze_ipv6=True):
    packet_info = {}
    packet_sizes = []  # List to store packet sizes
    # Iterate through packets and store information
    for idx, packet in enumerate(cap):
        if analyze_ipv4 and 'IP' in packet and 'UDP' in packet:
            if (packet.ip.src == src_ip and packet.ip.dst == dst_ip) or (packet.ip.src == dst_ip and packet.ip.dst == src_ip):
                src_port = packet.udp.srcport
                dst_port = packet.udp.dstport
                timestamp = float(packet.sniff_timestamp)
                length = int(packet.length)
                key = (src_ip, dst_ip, src_port, dst_port)
                if key not in packet_info:
                    packet_info[key] = {'sent': [{'timestamp': timestamp, 'length': length}], 'frame_number': idx + 1}
                else:
                    packet_info[key]['sent'].append({'timestamp': timestamp, 'length': length})
                    packet_info[key]['received'] = timestamp
                    packet_info[key]['frame_number_received'] = idx
                    packet_sizes.append(length)
        elif analyze_ipv6 and 'IPv6' in packet and 'UDP' in packet:
            src_port = packet.ipv6.src
            dst_port = packet.ipv6.dst
            timestamp = float(packet.sniff_timestamp)
            length = int(packet.length)
            key = (src_port, dst_port)
            if key not in packet_info:
                packet_info[key] = {'sent': [{'timestamp': timestamp, 'length': length}], 'frame_number': idx + 1}
            else:
                packet_info[key]['sent'].append({'timestamp': timestamp, 'length': length})
                packet_info[key]['received'] = timestamp
                packet_info[key]['frame_number_received'] = idx
                packet_sizes.append(length)

    # Data processing for metrics visualisation
    rtt_values, jitter_values, throughput_values, packet_loss_values = [], [], [], []
    for key, info in packet_info.items():
        if 'received' in info:
            rtt = info['received'] - info['sent'][0]['timestamp']
            jitter = sum(abs(info['sent'][i]['timestamp'] - info['sent'][i-1]['timestamp'] - rtt) for i in range(1, len(info['sent'])))
            total_bytes_sent = sum(packet['length'] for packet in info['sent'])
            throughput = (total_bytes_sent * 8) / (rtt / 1000000)  # Convert delay to seconds
            rtt_values.append(rtt)
            jitter_values.append(jitter)
            throughput_values.append(throughput)
            packet_loss_values.append(0)  # No packet loss for this example
            if 'frame_number_received' in info:
                print(f"Frame Number: {info['frame_number_received']}")
            print(f"RTT for {key}: {rtt} seconds")
            print(f"Jitter for {key}: {jitter} seconds")
            print(f"Throughput for {key}: {throughput} bits per second")
        else:
            rtt_values.append(None)
            jitter_values.append(None)
            throughput_values.append(None)
            packet_loss_values.append(1)  # 1 indicates packet loss
            print(f"Packet loss for {key}: No response received (Frame Number: {info['frame_number']})")

    # Plotting with adjusted figure size
    fig, axs = plt.subplots(3, 2, figsize=(12, 10))
    fig.suptitle(f'Network Metrics Over Time (Source: {src_ip}, Destination: {dst_ip})')
    axs[0, 0].plot(rtt_values, label='RTT')
    axs[0, 0].set_title('Round Trip Time (RTT)')
    axs[0, 0].set_ylabel('Time (seconds)')
    axs[0, 1].plot(jitter_values, label='Jitter')
    axs[0, 1].set_title('Jitter')
    axs[0, 1].set_ylabel('Time (seconds)')
    axs[1, 0].plot(throughput_values, label='Throughput')
    axs[1, 0].set_title('Throughput')
    axs[1, 0].set_ylabel('Bits per second')
    axs[1, 1].bar(range(len(packet_loss_values)), packet_loss_values, color='red', alpha=0.7, label='Packet Loss')
    axs[1, 1].set_title('Packet Loss')
    axs[1, 1].set_xlabel('Packet Index')
    axs[1, 1].set_ylabel('Packet Loss (1 indicates loss)')
    axs[2, 0].hist(packet_sizes, bins=50, color='green', alpha=0.7, label='Packet Size Distribution')
    axs[2, 0].set_title('Packet Size Distribution')
    axs[2, 0].set_xlabel('Packet Size (bytes)')
    axs[2, 0].set_ylabel('Frequency')
    axs[2, 1].axis('off')
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.show()

# Main 
while True:
    cap = load_capture_file()
    while True:
        print("Choose an option:")
        print("1. Identify Coexistence Method")
        print("2. Analyse Packet Data (IPv4)")
        print("3. Analyse Packet Data (IPv6)")
        print("4. Analyse IPv6 Usage")
        print("5. Exit")
        option = input("Enter option (1, 2, 3, 4, or 5): ")
        if option == '1':
            coexistence_method = identify_coexistence_method(cap)
            print(f"Coexistence Method: {coexistence_method}")
        elif option in ('2', '3'):
            source_ip = input("Enter the source IP address: ")
            destination_ip = input("Enter the destination IP address: ")
            if option == '2':
                calculate_metrics(cap, source_ip, destination_ip, analyze_ipv4=True, analyze_ipv6=False)
            elif option == '3':
                calculate_metrics(cap, source_ip, destination_ip, analyze_ipv4=False, analyze_ipv6=True)
        elif option == '4':
            analyze_ipv6_usage(cap)
        elif option == '5':
            print("Exiting program.")
            exit()
        else:
            print("Invalid option. Please enter a valid number (1, 2, 3, 4, or 5).")

