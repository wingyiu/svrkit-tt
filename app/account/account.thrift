
namespace py app.account.thf

enum AccountStatus {
	Normal = 0,
	BAN = 1,
}

struct AccountHandle {
	1: optional string username,
	2: optional string email,
	3: optional string phone,
}

struct Account {
	1: i32 account_id = 0,
	2: optional string username,
	3: optional string email,
	4: optional string phone,
	5: optional i32 created_at,
	6: optional i32 updated_at,
	7: optional i32 last_login,
	8: optional i32 status
}


exception AccountExisted {
}

service AccountService {

	string ping(1: i32 seq_id, 2: string ball),

	Account reg(1:i32 seq_id, 2: AccountHandle handle, 3: string password) throws (1: AccountExisted e),

	Account login(1:i32 seq_id, 2: AccountHandle handle, 3: string password),

	i32 change_pwd(1:i32 seq_id, 2: AccountHandle handle, 3: string password, 4: string new_password),


}
