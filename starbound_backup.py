# Foreword: Please make sure that you do not unpack a backup by accident! It might cause problems for existing saves that have not been backed up.

# === USER VARIABLES ===
# Fill these out!
backup = True # True/False (case sensitive). Are you trying to backup a file, or unpack an existing backup? When unpacking, try to make sure that there is no existing mod/universe/player data.
backup_name = "Dergie_FU1" # The name of the folder that the files will be saved to or unpacked from.
	# You can put the names of your backups here to remember them more easily! For example:
	# "Degie_27_04_2020", "Backup_number_9", "sfw_modlist"
steamapps_directory = "E:/Steam/steamapps/" # You'll need to provide the location of your steamapps directory here. I've left mine in as an example on how you should write a directory.
	# Remember that you should replace all \ characters with a / . Sorry! This is just how code is.


# Advanced variables
# These allow you to have much finer control over the program I've written. If you don't know what you're doing, don't worry about these!
delete_original_files = False # Whether my program should delete the current save data AFTER it backs it all up. They will still be saved in the backup location.
	# This WILL NOT delete mods you've subscribed to on the steam workshop. You have to manually unsubscribe from those, sorry!
overwrite_existing_backup = False # If a backup exists here already, should we just delete it when backing up?
auto_backup_destination = True # If you don't care where you files get backed up to, set this as "True" and I'll handle it all myself!
backup_destination = "E:/Steam/steamapps/common/Starbound/safety_backupy_place/" # The location you want the backup to be saved to or unpacked from if auto_backup_destination is set to "False"


# Licencing stuff:
# lol feel free to use it anywhere for whatever. Consider this as permission to be treated as a Public Domain licence.

# === EVERYTHING ELSE ===
# Don't touch this.
import pathlib
import shutil
import os


print("Running CrunchyDuck's Starbound backup script...\nThis may take a while. Please don't close this window until it says it's done!\nBecause like, you'll probably break something.")

class PathlibObj():
	"""After over a month of using pathlib I've found out this object is useless because I can just use str(path) to get the string version of a path. Over a dozen forums, and this was never mentioned."""
	string = ""
	path = ""

	def create(self, absolute_path):
		self.string = absolute_path
		self.path = pathlib.Path(absolute_path)

	def make_path(self):
		if not self.path.exists(): # Don't create a new dir if it already exists, dummy.
			os.makedirs(self.string)


def path_obj(directory):
	"""Simply returns a PathlibObj object with the create function already filled out."""
	hold = PathlibObj()
	hold.create(directory)
	return hold


def get_path_name(directory):
	dir_len = len(directory)
	filename = ""

	for i in range(dir_len):
		if directory[-i] == "\\":
			for j in range(i):
				filename = filename + directory[-i + j]
			break
	return filename


# Make sure the above syntax ends with a slash.
if backup_destination[-1] != "/" and backup_destination[-1] != "\\": backup_destination += "/"
if steamapps_directory[-1] != "/" and steamapps_directory[-1] != "\\": steamapps_directory += "/"


master_directory = path_obj(steamapps_directory) # Steam folder.

if master_directory.path.exists():
	if backup_name != "":
		if auto_backup_destination or backup_destination != "": # Ensure the user has filled out what is required for this.
			if steamapps_directory != "":
				mods_directory = path_obj(steamapps_directory + "workshop\\content\\211820\\") # Folder for steam mods.
				starbound_directory = path_obj(steamapps_directory + "common\\Starbound\\") # Starbound folder
				starbound_mods_directory = path_obj(starbound_directory.string + "mods\\") # Location of the mods folder in the starbound folder
				starbound_player_directory = path_obj(starbound_directory.string + "storage\\player\\")
				starbound_universe_directory = path_obj(starbound_directory.string + "storage\\universe\\")

				# The places we'll put each type of file that we want to backup.
				if auto_backup_destination: backup_folder_directory = path_obj(starbound_directory.string + "backups\\" + backup_name + "\\")
				else: backup_folder_directory = path_obj(backup_destination + backup_name + "\\") # Need to test this.

				backup_player = path_obj(backup_folder_directory.string + "player\\")
				backup_universe = path_obj(backup_folder_directory.string + "universe\\")
				backup_mods = path_obj(backup_folder_directory.string + "mods\\")

				check_file = pathlib.Path(backup_folder_directory.string + "do_not_delete.fox").exists()  # A file used to check if there's an existing backup here.

				if backup is True:
					if overwrite_existing_backup or not check_file: # If this file exists already, it means we've already got data packed here.
						userinput = ""
						if not check_file:
							if not backup_folder_directory.path.exists():  # Don't create a new dir if it already exists, dummy.
								os.makedirs(backup_folder_directory.string)
							with open(backup_folder_directory.string + "do_not_delete.fox", "w"): pass # Create a blank file to signify that we've packed data.
						else:
							print("Are you sure you want to delete your existing backup files at {0}? Type ABSOLUTELY if so, and anything else if not.".format(backup_folder_directory.string))
							userinput = input()
							if userinput == "ABSOLUTELY":
								# Delete all backed up files.
								f = [None, None, None]
								f[0] = list(backup_player.path.glob("*.*")) + list(backup_player.path.glob("metadata")) + list(backup_player.path.glob("statistics"))
								f[1] = list(backup_universe.path.glob("*.*"))
								f[2] = list(backup_mods.path.glob("*.pak"))
								for directory in f:
									for file in directory:
										os.remove(file)
							else:
								userinput = "cancel"
								print("Aborting backup...")

						if userinput != "cancel":
							print("Backing up files...")

							# If these directories don't exist already, create them.
							backup_player.make_path()
							backup_universe.make_path()
							backup_mods.make_path()


							# Get player files
							player_files = list(starbound_player_directory.path.glob("*.*")) + list(starbound_player_directory.path.glob("metadata")) + list(starbound_player_directory.path.glob("statistics"))
							for file in player_files:
								shutil.copy2(file, backup_player.string, follow_symlinks=False)
								if delete_original_files: os.remove(file)

							# Get universe files
							universe_files = list(starbound_universe_directory.path.glob("*.*"))
							for file in universe_files:
								shutil.copy2(file, backup_universe.string, follow_symlinks=False)
								if delete_original_files: os.remove(file)

							# Get mods
							starbound_mod_files = list(starbound_mods_directory.path.glob("*.pak")) # All mods within the starbound mod directory. These mods won't have their names changed.
							steam_mod_files = list(mods_directory.path.glob("**/*.pak")) # Get all .pak stored within the steam mod directory

							for mod in starbound_mod_files:
								shutil.copy2(mod, backup_mods.string, follow_symlinks=False) # I tried to use the "shutil.move" function, but couldn't seem to get it to work, so I'm copying and deleting instead :(
								if delete_original_files: os.remove(mod)

							for mod in steam_mod_files:
								# We'll need to rename all of these files, as they're all named "contents.pak".
								new = shutil.copy2(mod, backup_mods.string, follow_symlinks=False)
								mod_id = get_path_name((str(mod.parent)))
								name = backup_mods.string + get_path_name(str(mod.parent) + ".pak")
								try:
									os.rename(new, name)
								except OSError:
									print("Duplicate mod with the ID {0}".format(mod_id[1:]))
									os.remove(new) # Remove the file we just moved in so we don't have a duplicate in the future.

								# I won't delete these files as they're used by Steam itself, and I don't know what drawbacks this might have.


							print("Backup successful! Your saves can be found at {0}!\nThank you for using my dumb program <3 - CrunchyDuck".format(backup_folder_directory.string))

					else:
						print("A file has already been packed at {0}!\nPlease unpack it first, or delete all players, universes, mods and packed.fox files here.".format(backup_folder_directory.string))
				else:
					if check_file:
						print("Unpacking files...")
						# Player files
						player_files = list(backup_player.path.glob("*.*")) + list(backup_player.path.glob("metadata")) + list(backup_player.path.glob("statistics"))
						for file in player_files:
							shutil.copy2(file, starbound_player_directory.string, follow_symlinks=False)
							if delete_original_files: os.remove(file)


						# Get universe files
						universe_files = list(backup_universe.path.glob("*.*"))
						for file in universe_files:
							shutil.copy2(file, starbound_universe_directory.string, follow_symlinks=False)
							if delete_original_files: os.remove(file)

						# Get mods
						starbound_mod_files = list(backup_mods.path.glob("*.pak"))
						for mod in starbound_mod_files:
							shutil.copy2(mod, starbound_mods_directory.path, follow_symlinks=False)
							if delete_original_files: os.remove(mod)


						os.remove(backup_folder_directory.string + "do_not_delete.fox") # Delete my "flag" file to signify the space here is clear.
						print("Unpack finished! Have fun :)")

					else:
						print("There is no backup located at {0}.".format(backup_folder_directory.string))

			else:
				print("Please fill out the steamapps_directory field")
		else:
			print("auto_backup_destination is set to \"False\", please fill out the backup_destination field or change the settings.")

	else:
		print("backup_name has been left blank. Please provide the name of a file to backup to or unpack from!")

else:
	print("The directory {0} cannot be found.\nIs this the correct location of your steamapps directory?".format(steamapps_directory))

print("Press enter to close.")
input()

