import os
from VMCommandTranslationProvider import VMCommandTranslationProvider
from VMCommandType import VMCommandType

TEMP_LOCATION_IN_RAM = 5

ARG1_TRANSLATION = {'local': 'LCL',
                    'argument': 'ARG',
                    'this': 'THIS',
                    'that': 'THAT'}


class VMCodeWriter:

    def __init__(self):
        self.asm_file_name = None
        self.vm_file_name = None
        self.vm_file_name_without_dir = None

        self.command_translation_provider = VMCommandTranslationProvider('VMCommandsImplementationInHack')
        self.result = ''

    def setFileName(self, vm_file_name):
        self.vm_file_name = vm_file_name
        self.vm_file_name_without_dir = os.path.basename(vm_file_name).rsplit('.', maxsplit=1)[0].strip()

        if self.asm_file_name is None:
            if os.path.isfile(vm_file_name):
                self.asm_file_name = vm_file_name.rsplit('.', maxsplit=1)[0].strip()
            else:
                if vm_file_name.find('/') != -1:
                    self.asm_file_name = vm_file_name + '/' + vm_file_name.rsplit('/', maxsplit=1)[1]
            self.asm_file_name += '.asm'
            print(f'Resulting .asm file name: {self.asm_file_name}')

    def writeArithmetic(self, command_name, cur_cmd_ind):
        # self.result += ARITHMETIC_COMMANDS_TRANSLATION.get(command_name)(current_command_index)
        translated_command = self.command_translation_provider.get_command_translation(VMCommandType.C_ARITHMETIC,
                                                                                       command_name)
        if command_name in ['eq', 'gt', 'lt']:
            translated_command = translated_command.format(cur_cmd_ind, cur_cmd_ind, cur_cmd_ind, cur_cmd_ind)

        self.result += translated_command

    def writePushPop(self, command_type, command_name, segment, i):

        translated_command = self.command_translation_provider.get_command_translation(
            command_type, command_name, segment)

        if segment == 'constant':
            translated_command = translated_command.format(i)
        elif segment in ['local', 'argument', 'this', 'that']:
            translated_command = translated_command.format(i, ARG1_TRANSLATION.get(segment))
        elif segment == 'static':
            translated_command = translated_command.format(self.vm_file_name_without_dir, i)
        elif segment == 'temp':
            translated_command = translated_command.format(TEMP_LOCATION_IN_RAM, i)
        elif segment == 'pointer':
            new_segment = 'this' if int(i) == 0 else 'that'
            translated_command = translated_command.format(ARG1_TRANSLATION.get(new_segment))
        else:
            # TODO
            raise Exception(f'Segment {segment} is not implemented yet')

        self.result += translated_command

    def write_asm_file(self):
        asm_file = open(self.asm_file_name, 'w')
        asm_file.write(self.result)
        asm_file.close()
