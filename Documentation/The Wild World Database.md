# Tables
- Global Data = `GlobalData`
	- Holds globally accessed data, like `KeyType` given, and `DayCount`
- Players = `Players`
	- Holds all player profile data
- Jobs = `Jobs`
	- Holds all jobs existent within the game

# Accessing Database
Every interaction for every separate action *should* generate it's own cursor for any kind of interaction with the database.
This is an example of how that's done:

```Python
DayCount = 1

while True:
	await sleep(8)
	DayCount += 1
	Cursor = GlobalData.Database.Generate_Cursor()
	Cursor.execute("UPDATE GlobalData SET DayCount = ?", (DayCount,))
	GlobalData.Database.TWDCONNECTION.commit()
	Cursor.close()
```

I'll describe the steps in detail:
1. Instantiate new Cursor
`Cursor = GlobalData.Database.Generate_Cursor()`
2. Execute some kind of command
`Cursor.execute("SOME SQL COMMAND")`
3. Commit changes to database using `TWDCONNECTION`, which is a Connection Object that allows changes to actually be written to the database.
`GlobalData.Database.TWDCONNECTION.commit()`
4. Close the Cursor when we're done
`Cursor.close()`