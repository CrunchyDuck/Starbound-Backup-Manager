# Foreword: Please make sure that you do not unpack a backup by accident! It might cause problems for existing saves that have not been backed up.

# === USER VARIABLES ===
# Fill these out!
backup = True # Are you trying to backup a file, or unpack an existing backup?
backup_name = "Dergie_27_04_2020" # The name of the folder that the files will be saved to or unpacked from.

# Advanced variables
# These allow you to have much finer control over the program I've written. If you don't know what you're doing, don't touch these!
delete_original_files = True # Whether my program should delete the files stored in /universe, /players and /mods. They will still be saved in the backup location. This WILL NOT delete mods you've subscribed to on the steam workshop. You have to manually unsubscribe from those, sorry!
path_is_relative = False # Is the below "backup_destination" a relative path, or an absolute path? Don't change this if you don't know what you're doing.
auto_backup_destination = True # If you don't care where you files get backed up to, set this as "True" and I'll handle it all myself!
backup_destination = "E:\\Steam\\steamapps\\common\\Starbound\\safety_backupy_place" # The location you want the backup to be saved to or unpacked from. If you don't know how to fill out this field, don't touch it.
steamapps_directory = "E:\\Steam\\steamapps\\" # If "path_is_relative" is False, then you'll need to provide the location of your steamapps directory. I've left mine in as an example on how you should write a directory.


# I do not own a mac or a linux machine, so it'd be great if anyone who has one could tell me if this works fine or not!


# === EVERYTHING ELSE ===
# Don't touch this.
import pathlib
import shutil
import os


class PathlibObj():
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


if backup_name is not "":
	if not path_is_relative:
		if auto_backup_destination or (backup_destination is not ""): # Ensure the user has filled out what is required for this.
			if steamapps_directory is not "":

				if backup is True:
					master_directory = path_obj(steamapps_directory) # Steam folder.
					mods_directory = path_obj(steamapps_directory + "workshop\\content\\211820\\") # Folder for steam mods.
					starbound_directory = path_obj(steamapps_directory + "common\\Starbound\\") # Starbound folder
					starbound_mods_directory = path_obj(starbound_directory.string + "mods\\") # Location of the mods folder in the starbound folder
					starbound_player_directory = path_obj(starbound_directory.string + "storage\\player\\")
					starbound_universe_directory = path_obj(starbound_directory.string + "storage\\universe\\")

					# The places we'll put each type of file that we want to backup.
					if auto_backup_destination:
						backup_folder_directory = path_obj(starbound_directory.string + "backups\\" + backup_name + "\\")
					else: # Need to test this.
						backup_folder_directory = path_obj(backup_destination)

					if not pathlib.Path(backup_folder_directory.string + "packed.fox").exists(): # If this file exists already, it means we've already got data packed here.
						with open(backup_folder_directory.string + "packed.fox", "w"): pass # Create a blank file to signify that we've packed data.

						backup_player = path_obj(backup_folder_directory.string + "player\\")
						backup_universe = path_obj(backup_folder_directory.string + "universe\\")
						backup_mods = path_obj(backup_folder_directory.string + "mods\\")

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
							os.remove(mod)
							if delete_original_files: os.remove(mod)

						mod_number = 0
						for mod in steam_mod_files:
							# We'll need to rename all of these files, as they're all named "contents.pak".
							new = shutil.copy2(mod, backup_mods.string, follow_symlinks=False)
							name = backup_mods.string + str(mod_number) + ".pak"
							os.rename(new, name)

							# I won't delete these files as they're used by Steam itself, and I don't know what drawbacks this might have.
							mod_number += 1
							pass


						print("Backup successful! Your saves can be found at {0}!\nThank you for using my dumb program <3 - CrunchyDuck".format(backup_folder_directory.string))

					else:
						print("A file has already been packed at {0}! Please unpack it first, or delete all players, universes, mods and packed.fox files here.".format(backup_folder_directory.string))

				else:
					# Unpack files
					pass


			else:
				print("path_is_relative is set to \"True\", please fill out the steamapps_directory field or change path_is_relative to \"False\"")
		else:
			print("path_is_relative is set to \"True\" and auto_backup_destination is set to \"False\", please fill out the backup_destination field or change the settings.")

	else:
		# Relative path code.
		pass



	#current_dir = PathlibObj()
	#current_dir.create(os.getcwd())


else:
	print("backup_name has been left blank. Please provide the name of a file to backup to or unpack from!")


