import requests
import time

class Colors:
    GREEN = "\033[92m"  
    RED = "\033[91m"    
    YELLOW = "\033[93m" 
    RESET = "\033[0m"   

def read_authorization():
    with open("authorization.txt", "r") as file:
        return [line.strip() for line in file if line.strip()]

def get_total_cats(headers):
    url_user = "https://api.catshouse.club/user"
    response_user = requests.get(url_user, headers=headers)
    if response_user.status_code == 200:
        user_data = response_user.json()
        return user_data.get("totalRewards", 0), user_data.get("username", "Unknown")
    return 0, "Unknown"

def process_tasks(authorization_data):
    headers = {
        "Sec-Ch-Ua": "\"Chromium\";v=\"128\", \"Not;A=Brand\";v=\"24\", \"Microsoft Edge\";v=\"128\", \"Microsoft Edge WebView2\";v=\"128\"",
        "Sec-Ch-Ua-Platform": "\"Windows\"",
        "Sec-Ch-Ua-Mobile": "?0",
        "Authorization": f"tma {authorization_data}",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0",
        "Content-Type": "application/json",
        "Accept": "*/*",
        "Origin": "https://cats-frontend.tgapps.store",
        "Referer": "https://cats-frontend.tgapps.store/",
    }

    total_cats_before, username = get_total_cats(headers)
    print(f"username: {username} - Total CATS: {total_cats_before}")

    url_tasks = "https://api.catshouse.club/tasks/user?group=cats"
    response_tasks = requests.get(url_tasks, headers=headers)
    
    if response_tasks.status_code == 200:
        tasks_data = response_tasks.json().get("tasks", [])
        for task in tasks_data:
            task_id = task.get("id")
            task_title = task.get("title", "No Title")
            reward_points = task.get("rewardPoints", 0)

            start_time = time.time()  
            if task_id == 104:
                print(f"{Colors.YELLOW}Melakukan check untuk Task ID {task_id}: {task_title} - Reward Points: {reward_points}{Colors.RESET}")
                if not check_task(task_id, headers):
                    continue  
            elif task_id in [59, 110, 107, 51, 1, 13, 14]:
                print(f"Melakukan completed dan check untuk Task ID {task_id}: {task_title} - Reward Points: {reward_points}")
                if not complete_task(task_id, headers) or not check_task(task_id, headers):
                    continue
            elif task_id not in [105, 99, 5, 2, 3, 4]:
                print(f"Melakukan complete untuk Task ID {task_id}: {task_title} - Reward Points: {reward_points}")
                if not complete_task(task_id, headers):
                    continue
            else:
                print(f"{Colors.YELLOW}Task ID {task_id} diskip: {task_title} - Reward Points: {reward_points}{Colors.RESET}")

            elapsed_time = time.time() - start_time
            if elapsed_time > 60: 
                print(f"{Colors.RED}Waktu respons melebihi batas untuk Task ID {task_id}. Melanjutkan ke tugas berikutnya.{Colors.RESET}")
                continue

        total_cats_after, _ = get_total_cats(headers)
        print(f"Total CATS sebelumnya: {total_cats_before} | Total CATS setelah: {total_cats_after}")
    else:
        print(f"{Colors.RED}Failed to get tasks data. Status code: {response_tasks.status_code}{Colors.RESET}")

def complete_task(task_id, headers):
    url_complete = f"https://api.catshouse.club/tasks/{task_id}/complete"
    try:
        response_complete = requests.post(url_complete, headers=headers, json={}, timeout=60)
        if response_complete.status_code == 200:
            print(f"{Colors.GREEN}Task ID {task_id} completed successfully.{Colors.RESET}")
            return True
        else:
            print(f"{Colors.RED}Failed to complete Task ID {task_id}. Status code: {response_complete.status_code}{Colors.RESET}")
            return False
    except requests.Timeout:
        print(f"{Colors.RED}Request to complete Task ID {task_id} timed out.{Colors.RESET}")
        return False

def check_task(task_id, headers):
    url_check = f"https://api.catshouse.club/tasks/{task_id}/check"
    try:
        response_check = requests.post(url_check, headers=headers, json={}, timeout=60)
        if response_check.status_code == 200:
            check_result = response_check.json()
            print(f"Task ID {task_id} check result: {check_result}")
            return True
        else:
            print(f"{Colors.RED}Failed to check Task ID {task_id}. Status code: {response_check.status_code}{Colors.RESET}")
            return False
    except requests.Timeout:
        print(f"{Colors.RED}Request to check Task ID {task_id} timed out.{Colors.RESET}")
        return False

if __name__ == "__main__":
    authorization_list = read_authorization()
    for idx, authorization_data in enumerate(authorization_list, start=1):
        print(f"Akun {idx}:")
        process_tasks(authorization_data)
