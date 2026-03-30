function [source_struct, source_name, param1, param2] = generate_source_params(Source_Type, number_bins)


    switch Source_Type
        case 1
            source_struct = generate_quake_params();
            source_name = 'quake';
            param1 = source_struct.Slip;
            param2 = source_struct.Length;


        case 2
            source_struct = generate_dyke_params();
            source_name = 'dyke';
            param1 = source_struct.Opening;
            param2 = source_struct.Length;


        case 3
            source_struct = generate_sill_params();
            source_name = 'sill';
            param1 = source_struct.Opening;
            param2 = source_struct.Depth;


        case 4
            number_bins = 4;
            d_bin = randi(number_bins);
            v_bin = randi(number_bins);

            source_struct = generate_mogi_params(d_bin, v_bin, number_bins);
            source_name = 'mogi';
            param1 = source_struct.Depth;
            param2 = source_struct.Volume;

        case 5
            source_struct = generate_penny_params();
            source_name = 'penny';
            param1 = source_struct.Depth;
            param2 = source_struct.Pressure;

        otherwise
            error('Invalid Source_Type. Must be 1 to 5.');
    end
end