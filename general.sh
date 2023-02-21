# Forensic Script
# Created By Jordan Kasoff (jmk9298@rit.edu)


#!/bin/bash




#Welcome Message
echo ""
echo "Forensic Script V1.2"
echo "Created By Jordan Kasoff"
echo ""
echo "Please note, SUDO is required"

#Global Settings
brief_output=0
while getopts "b:" OPTION; do
    case "${OPTION}" in
        b)
          brief_output=1 #true (boolean)
          echo "Brief Mode Engaged"
          ;;
    esac
done


#Prepare to save report to same storage location as Script
#Thought: Ideally Script will be on USB, and this will save report on same media
#Get directory of the script, create report file in same location
redirect_output() {
	location=$(pwd)
	filename="report.txt"
	final_location=$location"/"$filename
	if test -f "$final_location"; then #check if file exists
		echo "$final_location exists, rewriting"
		echo "Forensic Report"  > $final_location #rewrite file with title
		echo  " " >> $final_location #append to file
	else
		touch $final_location #create file if it does not
		echo "File Created"
	fi

}
redirect_output


# Send time data to final location
get_time_data() {
	curr_time=$(date) #save current time (date) to variable "curr_time"
	time_up=$(uptime)
	echo "System Time: " $curr_time >> $final_location # append variable to file
	echo "Uptime:" $time_up >> $final_location
	echo ""
	echo "Wrote Time Data"
}

get_time_data


get_OS_data(){
	operating_name=$(hostnamectl |grep "Operating System")
	cpu_info=$(lscpu |grep "Model name")
	typical_name=$(hostnamectl |grep "Icon name")
	kernel_name=$(hostnamectl |grep "Kernel")
	echo $operating_name >> $final_location
	echo $cpu_info >> $final_location
	echo $typical_name >> $final_location
	echo $kernel_name >> $final_location
	echo ""
	echo "Wrote OS Data"
}

get_OS_data


get_system_data(){
	architecture=$(hostnamectl |grep "Architecture")
	memory=$(free -h)
	storage=$(df -h)
	partition=$(sudo fdisk -l) #requires sudo permission
	host_name=$(hostname)
	domain_name=$(domainname)

	echo $architecture >> $final_location
	echo " " >> $final_location
	echo "Memory Information" >> $final_location
	echo " " >> $final_location
	printf "%s\n" "$memory" >> $final_location #preserve line spacing
	echo " " >> $final_location
	echo "Storage Information" >> $final_location
	echo " " >> $final_location
	printf "%s\n" "$storage" >> $final_location #preserve line spacing
	echo " " >> $final_location
	echo "Partition Information" >> $final_location
	echo " " >> $final_location
	printf "%s\n" "$partition" >> $final_location
	echo " " >> $final_location
	echo "Hostname: " $host_name >> $final_location
	if [[ "$domain_name" = "(none)" ]]; then
	 	echo "No Domain Name" >> $final_location
	else
		echo $domain_name >> $final_location
	fi
	echo ""
	echo "Wrote System Data"
}

get_system_data


get_network_data(){
	echo "" >> $final_location
	echo "Netowrk Information:" >> $final_location
	for interface in $(ls /sys/class/net)
	do

		echo "Interface: " $interface >> $final_location
		echo -n " " >> $final_location
		cat /sys/class/net/$interface/address >> $final_location
		echo $(ip -f inet addr show $interface |grep inet)>>$final_location
		prom_statement=$(ip -f inet addr show $interface |grep "PROMISC")
		if [ -z "$prom_statement" ];
		then
			echo ""
		else
			echo "Promiscious Mode Enabled" >> $final_location
		fi
		echo " " >> $final_location
	done

	echo "Running NetStat, please wait"
	if [ "$brief_output" -eq "0" ];
	then
		network_conn=$(netstat)
	else
		network_conn=$(netstat|head -n 15)
	fi
	printf "%s\n"  "$network_conn" >> $final_location

	echo ""
	echo "Wrote Network Data"
}
get_network_data


get_user_data(){
	logged_in=$(who)
	logged_out=$(last)
	root_uid=$(awk -F: '($3 == 0) {printf "%s:%s\n",$1,$3}' /etc/passwd)

	echo " " >> $final_location
	echo " " >> $final_location
	echo "Users Logged in" >> $final_location
	printf "%s\n" "$logged_in" >> $final_location
	echo " " >> $final_location
	echo "User Session History: " >> $final_location
	printf "%s\n" "$logged_out" >> $final_location
	echo " " >> $final_location
	echo "Users with UID=0: " >> $final_location
	printf "%s\n" "$root_uid" >> $final_location
	echo ""
	echo "" >> $final_location
	echo "SUID - Root Files: " >> $final_location
	if [ "$brief_output" -eq "0" ];
	then
		suid_files=$(find / -uid 0 -perm -4000 2>/dev/null)
	else
		suid_files=$(find / -uid 0 -perm -4000 2>/dev/null|head -n 15)
	fi
	printf "%s\n"  "$suid_files" >> $final_location
	echo "Wrote User Data"

}

get_user_data


get_process_data(){
	echo " " >> $final_location
	echo " " >> $final_location
	echo "Process List:" >> $final_location
	if [ "$brief_output" -eq "0" ];
	then
		proc_list=$(ps ax)
	else
		proc_list=$(ps ax|head -n 5)
	fi
	printf "%s\n"  "$proc_list" >> $final_location
	echo ""

	echo " " >> $final_location
	echo "NetCat Files List:" >> $final_location
	if [ "$brief_output" -eq "0" ];
	then
		net_list=$(lsof -c nc)
	else
		net_list=$(lsof -c nc |head -n 5)
	fi
	printf "%s\n"  "$net_list" >> $final_location
	echo ""

	echo " " >> $final_location
	echo "Unlinked Files List:" >> $final_location
	if [ "$brief_output" -eq "0" ];
	then
		delete_list=$(lsof +L1)
	else
		delete_list=$(lsof +L1 |head -n 5)
	fi
	printf "%s\n"  "$delete_list" >> $final_location
	echo ""

	echo "Wrote Process Data"
}

get_process_data


get_other_data(){
	echo " " >> $final_location
	echo " " >> $final_location
	echo "Recently Modified Files List:" >> $final_location
	if [ "$brief_output" -eq "0" ];
	then
		modify_list=$(find /home -mtime -1)
	else
		modify_list=$(find /home -mtime -1|head -n 5)
	fi
	printf "%s\n"  "$modify_list" >> $final_location
	echo "" >> $final_location

	echo "Root Cron Tasks Sched:" >> $final_location
	task_list=$(sudo crontab -u root -l)
	printf "%s\n"  "$task_list" >> $final_location
	echo "" >> $final_location

	echo "SSH connections" >> $final_location
	ssh_list=$(netstat -a | grep ssh)
	printf "%s\n"  "$ssh_list" >> $final_location
	echo "" >> $final_location

	echo "ARP Table" >> $final_location
	arp_list=$(arp | head -n 5)
	printf "%s\n"  "$arp_list" >> $final_location
	echo "" >> $final_location

	echo "Command History" >> $final_location
	history_list=$(history | head -n 5)
	printf "%s\n"  "$history_list" >> $final_location
	echo "" >> $final_location

	echo ""

	echo "Wrote Others Data"


}

get_other_data

echo "Report Complete"
