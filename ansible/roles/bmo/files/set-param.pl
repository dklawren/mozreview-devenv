#!/usr/bin/perl -w
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

use strict;
use warnings;
use FindBin qw( $RealBin );
use lib "$RealBin/..";

use Bugzilla;
use Bugzilla::Config qw( :admin );
use Bugzilla::Constants;
Bugzilla->usage_mode(USAGE_MODE_CMDLINE);

my $params = Bugzilla->params;

my ($param_name, $param_value) = @ARGV;
die "Syntax: $0 param_name param_value\n" unless defined($param_value);
die "Invalid param name: $param_name\n" unless exists $params->{$param_name};

if ($params->{$param_name} ne $param_value) {
    SetParam($param_name, $param_value);
    write_params();
    print "'$param_name' set to '$param_value'\n";
} else {
    print "'$param_name' is already '$param_value'\n";
}
